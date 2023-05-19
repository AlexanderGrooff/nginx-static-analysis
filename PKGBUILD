# Maintainer: Alexander Grooff <alexandergrooff@gmail.com>
pkgname=nginx-static-analysis-git
pkgver=0.2.6
pkgrel=1
pkgdesc="Static analysis tool of Nginx configuration files"
url="https://github.com/AlexanderGrooff/nginx-static-analysis"
arch=("any")
license=("MIT")
groups=()
depends=()
makedepends=("git" "python-build" "python-installer" "python-wheel")
provides=("${pkgname%-git}")
conflicts=("${pkgname%-git}")
replaces=()
backup=()
options=()
install=
source=("git+${url}")
noextract=()
md5sums=('SKIP')

pkgver() {
    cd "$srcdir/${pkgname%-git}"
    grep -oP '(?<=version=")[^"]+' setup.py
}

build() {
    cd "$srcdir/${pkgname%-git}"
    python -m build --wheel --no-isolation
}

package() {
    cd "$srcdir/${pkgname%-git}"
    python -m installer --destdir="$pkgdir" dist/*.whl
}