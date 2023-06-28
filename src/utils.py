import platform
from enum import Enum
from typing import Self


class Site(Enum):
    """Supported Recordpool websites."""

    BANDCAMP = "Bandcamp"
    BEATJUNKIES = "Beatjunkies"
    BPMSUPREME = "BPMSupreme"
    DJCITY = "DJCity"

    # Not using StrEnum here since that will use the variable name in lowercase,
    # and I want to maintain the correct formatting for each name.
    def __str__(self) -> str:
        return self.value


class Platform(Enum):
    """OS platform enum."""

    LINUX = "Linux"
    MAC = "macOS"
    WINDOWS = "Windows"

    def is_linux(self) -> bool:
        """Returns true if on Linux."""
        return self == Platform.LINUX

    def is_mac(self) -> bool:
        """Return true if on macOS."""
        return self == Platform.MAC

    def is_windows(self) -> bool:
        """Returns true if on Windows."""
        return self == Platform.WINDOWS

    @classmethod
    def get(cls) -> Self:
        """Initialize Platform enum for current OS."""
        platform_name = platform.system().lower()
        if platform_name == "darwin":
            return Platform.MAC
        elif platform_name == "windows":
            return Platform.WINDOWS
        elif platform_name == "linux":
            return Platform.LINUX

        raise RuntimeError(f"Unsupported OS: '{platform.system()}'")

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
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
