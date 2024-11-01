destdir := home_dir() / ".local" / "image"
ts      := shell("date +%Y%m%d%H%M%S")
ext     := ".ociarchive"
name    := ts + ext
target  := destdir / name

build:
    buildah bud -t oci-archive:{{target}} Containerfile
    sudo bootc switch --transport=oci-archive {{target}}
    find {{destdir}} -type f -name "*{{ext}}" | sort -r | tail -n+3 | xargs rm -f
