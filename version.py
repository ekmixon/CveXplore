import os
import re
import subprocess

_PKG_DIR = os.path.dirname(__file__)


def _version_from_git_describe():
    """

    Read the version from ``git describe``. It returns the latest tag with an
    optional suffix if the current directory is not exactly on the tag.

    Example::

        $ git describe --always
        v2.3.2-346-g164a52c075c8

    The tag prefix (``v``) and the git commit sha1 (``-g164a52c075c8``) are
    removed if present.

    If the current directory is not exactly on the tag, a ``.devN`` suffix is
    appended where N is the number of commits made after the last tag.

    Example::

    '>>> _version_from_git_describe()'
    '2.3.2.dev346'

    """
    if not os.path.isdir(os.path.join(_PKG_DIR, ".git")):  # noqa: E501
        raise ValueError("not in git repo")

    process = subprocess.Popen(
        ["git", "describe", "--always"],
        cwd=_PKG_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    out, err = process.communicate()

    if process.returncode != 0:
        raise subprocess.CalledProcessError(process.returncode, err)
    tag = out.decode().strip()
    return (
        f"{match.group(1)}.dev{match.group(2)}"
        if (match := re.match("^v?(.+?)-(\\d+)-g[a-f0-9]+$", tag))
        else re.sub("^v", "", tag)
    )


def _version():
    version_file = os.path.join(_PKG_DIR, "CveXplore/VERSION")
    try:
        tag = _version_from_git_describe()
        # successfully read the tag from git, write it in VERSION for
        # installation and/or archive generation.
        with open(version_file, "w") as fdesc:
            fdesc.write(tag)
        return tag
    except Exception:
        # failed to read the tag from git, try to read it from a VERSION file
        try:
            with open(version_file, "r") as fdsec:
                tag = fdsec.read()
            return tag
        except Exception:
            # Rely on git archive "export-subst" git attribute.
            # See 'man gitattributes' for more details.
            git_archive_id = "$Format:%h %d$"
            sha1 = git_archive_id.strip().split()[0]
            if match := re.search("tag:(\\S+)", git_archive_id):
                return "git-archive.dev" + match[1]
            elif sha1:
                return f"git-archive.dev{sha1}"
            else:
                return "unknown.version"


VERSION = __version__ = _version()
VERSION_MAIN = re.search(r"[0-9.]+", VERSION).group()
