from django.db import models
from powershell import powershell
from django.db.models.query import QuerySet
from django.db.models import Count
from django.utils import timezone
import datetime


class SoftwareManager(models.Manager):
    def with_client_count(self):
        return (
            self.values("id", "name", "version")
            .annotate(clients=Count("computer"))
            .exclude(clients=0)
            .order_by("name", "version")
        )


class Software(models.Model):
    name = models.CharField(max_length=150)
    version = models.CharField(max_length=50, null=False)
    objects = SoftwareManager()

    class Meta:
        ordering = ["name", "version"]
        constraints = [
            models.UniqueConstraint(
                fields=["name", "version"], name="name of constraint"
            )
        ]

    def __str__(self) -> str:
        return self.name


class ComputerQuerySet(QuerySet):
    def update_ip(self):
        hostnames = list(self.values_list("hostname", flat=True))
        computers = []
        for (hostname, out, err) in powershell.get_ip_address(hostnames):
            computer = self.filter(hostname=hostname)[0]
            if "Host not found" in err:
                computer.status = "Error: Host not found"
            elif err != "":
                raise ValueError(err)
            else:
                computer.ip = out
                computer.status = "ok"
            computer.date_modified = timezone.now()
            computers.append(computer)
        return self.bulk_update(computers, fields=["status", "ip", "date_modified"])

    def update_network_status(self):
        self = self.exclude(status="Error: Host not found")
        hostnames = list(self.values_list("hostname", flat=True))
        computers = []
        for (hostname, out, err) in powershell.get_network_status(hostnames):
            computer = self.filter(hostname=hostname)[0]
            if "cannot ping device" in err:
                computer.status = "Error: Offline"
            elif err != "":
                raise ValueError(err)
            else:
                computer.status = "ok"
            computers.append(computer)
            computer.date_modified = timezone.now()
        return self.bulk_update(computers, fields=["status", "date_modified"])

    def update_remoting_status(self):
        self = self.exclude(status="Error: Host not found").exclude(
            status="Error: Offline"
        )
        hostnames = list(self.values_list("hostname", flat=True))
        computers = []
        for (hostname, out, err) in powershell._start_script_generator(
            "get_remoting_status", hostnames
        ):
            computer = self.filter(hostname=hostname)[0]
            if "powershell remoting not enabled" in err:
                computer.status = "Error: Remoting not Enabled"
            elif err != "":
                raise ValueError(err)
            else:
                computer.status = "ok"
            computers.append(computer)
            computer.date_modified = timezone.now()
        return self.bulk_update(computers, fields=["status", "date_modified"])

    def update_software(self):
        self = (
            self.exclude(status="Error: Remoting not Enabled")
            .exclude(status="Error: Host not found")
            .exclude(status="Error: Offline")
        )
        hostnames = list(self.values_list("hostname", flat=True))

        for (hostname, out) in powershell.get_software(hostnames):
            computer = self.get(hostname=hostname)
            softwares = []
            for software_out in out:
                name = software_out[0]
                version = software_out[1] if software_out[1] != "" else "unknown"
                if "Update for Microsoft" in name or "Microsoft Visual C++" in name:
                    continue
                software = Software.objects.filter(name=name).filter(version=version)
                if software.exists():
                    softwares.append(software[0])
                else:
                    software = Software(name=name, version=version)
                    software.save()
                    softwares.append(software)
            computer.software.set(softwares)

    def enable_remoting(self):
        self = (
            self.exclude(status="Error: Host not found")
            .exclude(status="Error: Offline")
            .exclude(status="ok")
        )
        hostnames = list(self.values_list("hostname", flat=True))
        powershell.enable_remoting(hostnames)


# Create your models here.
class ComputerManager(models.Manager):
    _queryset_class = ComputerQuerySet

    def sync_ad(self):
        ad_devices = powershell.get_ad_devices()
        computers = []
        # Create Devices
        for hostname in ad_devices:
            if hostname == "":
                continue
            if self.filter(hostname=hostname).exists():
                continue
            else:
                computers.append(self.model(hostname=hostname))
        # Delete not present
        for computer in self.all().exclude(hostname__in=ad_devices):
            print("Deleting: ", computer)
            computer.delete()
        return self.bulk_create(computers)


class Computer(models.Model):
    hostname = models.CharField(unique=True, max_length=15)
    ip = models.CharField(max_length=15)
    status = models.CharField(max_length=30)
    software = models.ManyToManyField(Software)
    date_modified = models.DateTimeField()

    objects = ComputerManager()

    class Meta:
        ordering = ["hostname"]

    def __str__(self) -> str:
        return self.hostname
