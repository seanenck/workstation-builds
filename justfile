destdir := home_dir() / ".local" / "image"
ts      := shell("date +%Y%m%d%H%M%S")
hash    := `git log -n 1 --format=%h`
ext     := ".ociarchive"
name    := ts + "." + hash + ext
target  := destdir / name

build:
    buildah bud -t oci-archive:{{target}} Containerfile
    sudo bootc switch --transport=oci-archive {{target}}
    find {{destdir}} -type f -name "*{{ext}}" | sort -r | tail -n+3 | xargs rm -f
