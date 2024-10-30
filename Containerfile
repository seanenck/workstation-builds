ARG release=41
ARG variant=sericea

FROM quay.io/fedora-ostree-desktops/$variant:$release
RUN dnf5 install --setopt=install_weak_deps=False -y \
    age \
    alacritty \
    ripgrep \
    ShellCheck \
    git-delta \
    just \
    binutils \
    neovim \
    bat && \
    dnf5 remove -y \
    foot && \
    dnf clean all && \
    ostree container commit
