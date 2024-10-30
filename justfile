destdir := "/var/cache/image"
workdir := env_var('HOME') / "Downloads"
name    := "system.ociarchive"
image   := workdir / name
target  := destdir / name

full: build deploy

build:
    buildah bud -t oci-archive:{{image}} Containerfile

deploy:
    test -e {{target}} && sudo mv {{target}} {{target}}.last
    sudo mv {{image}} {{target}}
    sudo bootc switch --transport=oci-archive {{target}}
