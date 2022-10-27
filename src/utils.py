import platform
from enum import Enum


class Site(Enum):
    """Supported Recordpool websites."""

    BANDCAMP = "Bandcamp"
    BEATJUNKIES = "Beatjunkies"
    BPMSUPREME = "BPMSupreme"
    DJCITY = "DJCity"

    # Not using StrEnum here since that will use the variable name in lowercase,
    # and I want to maintain the correct formatting for each name.
    def __str__(self):
        return self.value


class Platform(Enum):
    """OS platform."""

    LINUX = "Linux"
    MAC = "macOS"
    WINDOWS = "Windows"

    def is_linux(self):
        """Returns true if on Linux."""
        return self == Platform.LINUX

    def is_mac(self):
        """Return true if on macOS."""
        return self == Platform.MAC

    def is_windows(self):
        """Returns true if on Windows."""
        return self == Platform.WINDOWS

    @staticmethod
    def get():
        """Initialize Platform enum for current OS."""
        platform_name = platform.system().lower()
        if platform_name == "darwin":
            return Platform.MAC
        elif platform_name == "windows":
            return Platform.WINDOWS
        elif platform_name == "linux":
            return Platform.LINUX

        raise RuntimeError(f"Unsupported OS: '{platform.system()}'")

    def __str__(self):
        return self.value

    def __repr__(self):
        """Format platform name with version info."""
        if self.is_windows():
            (release, version, *others) = platform.win32_ver()
            try:
                build_version = int(version.split(".")[-1])
                # Windows 11 is still numbered as version 10, but we can check build number
                if build_version > 2200:
                    release = 11
            except ValueError:
                build_version = version

            # For example: 'Windows 11 Professional 22621'
            return f"{self.value} {release} {platform.win32_edition()} {build_version}"

        # For example: 'macOS 12.6 x86_64'
        return f"{self.value} {platform.mac_ver()[0]} {platform.machine()}"
