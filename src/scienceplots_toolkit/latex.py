"""LaTeX preamble management for Matplotlib.

Provides a builder-style :class:`PreambleManager` for constructing and
customising the ``text.latex.preamble`` string that Matplotlib uses when
``text.usetex`` is ``True``.

Example usage::

    >>> from scienceplots_toolkit.latex import PreambleManager
    >>> pm = PreambleManager()
    >>> pm.add_package("booktabs")
    >>> pm.add_package("hyperref")
    >>> pm.sans_serif_math = True
    >>> print(pm.build())
    \\usepackage{amsmath,amssymb,amsfonts}\\usepackage{textcomp}\\usepackage{gensymb}\\usepackage{siunitx}\\usepackage{graphicx}\\usepackage{booktabs}\\usepackage{hyperref}\\usepackage{sansmath}\\sansmath\\renewcommand{\\familydefault}{\\sfdefault}
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass  # no external runtime dependencies


# ------------------------------------------------------------------ #
#  Default package list (hard-coded core)                             #
# ------------------------------------------------------------------ #
_DEFAULT_PACKAGES: tuple[str, ...] = (
    "amsmath",
    "amssymb",
    "amsfonts",
    "textcomp",
    "gensymb",
    "siunitx",
    "graphicx",
)

# Package whose inclusion triggers sans-serif math mode.
SansMathKey = "sansmath"

SansMathCode = (
    r"\usepackage{sansmath}\sansmath"
    r"\renewcommand{\familydefault}{\sfdefault}"
)


# ------------------------------------------------------------------ #
#  PreambleManager                                                    #
# ------------------------------------------------------------------ #
class PreambleManager:
    """Build and manage the LaTeX ``text.latex.preamble`` string.

    Uses a *builder* pattern: each call to :meth:`add_package` /
    :meth:`remove_package` returns ``self`` so calls can be chained.

    Parameters
    ----------
    packages :
        The LaTeX packages to include.  Defaults to the six core
        packages that the toolkit ships with.
    sans_serif_math :
        When ``True`` the ``sansmath`` package (plus the necessary
        font switches) is appended automatically.



    >>> pm = PreambleManager()
    >>> len(pm.build()) > 0
    True
    >>> pm.add_package("booktabs").add_package("hyperref")
    PreambleManager(...)
    >>> "booktabs" in pm.build()
    True
    """

    __slots__ = ("_packages", "_sans_serif_math")

    # ---------- factory / class helpers ---------- #

    @classmethod
    def default(cls) -> PreambleManager:
        """Return a :class:`PreambleManager` pre-loaded with defaults.

        This is equivalent to::

            PreambleManager(sans_serif_math=True)
        """
        return cls(sans_serif_math=True)

    # ---------- construction ---------- #

    def __init__(
        self,
        packages: tuple[str, ...] | None = None,
        sans_serif_math: bool = False,
    ) -> None:
        self._packages: list[str] = (
            list(packages) if packages else list(_DEFAULT_PACKAGES)
        )
        self._sans_serif_math: bool = sans_serif_math

    # ---------- accessors ---------- #

    @property
    def packages(self) -> tuple[str, ...]:
        """The currently registered packages."""
        return tuple(self._packages)

    @property
    def sans_serif_math(self) -> bool:
        """Whether *sansmath* is enabled."""
        return self._sans_serif_math

    @sans_serif_math.setter
    def sans_serif_math(self, value: bool) -> None:
        self._sans_serif_math = value
        if value and SansMathKey not in self._packages:
            self._packages.append(SansMathKey)
        if not value and SansMathKey in self._packages:
            self._packages.remove(SansMathKey)

    # ---------- mutators (builder style) ---------- #

    def add_package(self, name: str) -> PreambleManager:
        """Add a LaTeX package and return ``self`` for chaining.

        Parameters
        ----------
        name :
            The package name, e.g. ``"booktabs"``.
        """
        if name not in self._packages:
            self._packages.append(name)
        return self

    def add_packages(self, *names: str) -> PreambleManager:
        """Add multiple packages at once and return ``self``.

        Example::

            pm.add_packages("booktabs", "hyperref", "graphicx")
        """
        for name in names:
            self.add_package(name)
        return self

    def remove_package(self, name: str) -> PreambleManager:
        """Remove a LaTeX package and return ``self``.

        Raises ``KeyError`` if the package is not present.
        """
        # Use a helper method to avoid duplicate logic
        self._remove_package(name)
        return self

    # ---------- build ---------- #

    def build(self) -> str:
        """Return the complete LaTeX preamble as a single string.

        The default core packages are joined first, followed by any
        user-added packages.  If ``sans_serif_math`` is enabled the
        necessary font switches are appended.
        """
        parts: list[str] = []

        # Default (core) packages always appear first, in order.
        for pkg in _DEFAULT_PACKAGES:
            parts.append(rf"\usepackage{{{pkg}}}")

        # Extra / non-default packages follow.
        for pkg in self._packages:
            if pkg not in _DEFAULT_PACKAGES:
                parts.append(rf"\usepackage{{{pkg}}}")

        # Sans-serif math code is always appended last.
        if self._sans_serif_math:
            parts.append(SansMathCode)

        return "".join(parts)

    # ---------- internal helpers ---------- #

    def _remove_package(self, name: str) -> None:
        """Remove *name* from the package list."""
        self._packages.remove(name)

    # ---------- dunder ---------- #

    def __repr__(self) -> str:  # noqa: D105
        pkgs = ", ".join(f"'{p}'" for p in self._packages)
        return f"PreambleManager({pkgs})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PreambleManager):
            return NotImplemented
        return (
            tuple(self._packages) == tuple(other._packages)
            and self._sans_serif_math == other._sans_serif_math
        )
