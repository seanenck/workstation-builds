destdir := home_dir() / ".local" / "image"
workdir := home_dir() / "Downloads"
name    := "system.ociarchive"
image   := workdir / name
target  := destdir / name

full: build deploy

build:
    buildah bud -t oci-archive:{{image}} Containerfile

deploy:
    test ! -e {{target}} || mv {{target}} {{target}}.last
    mv {{image}} {{target}}
    sudo bootc switch --transport=oci-archive {{target}}
