#! /bin/sh
set -e

export DISPLAY=:99.0

if [ "${BITS}" = "64" ]; then
    MSI_END=".amd64.msi"
    WINE="wine64"
else
    MSI_END=".msi"
    WINE="wine"
fi

if [ "${TRAVIS_PYTHON_VERSION}" = "2.6" ]; then
    PYTHON_MSI="python-2.6.6${MSI_END}"
    PYTHON_URL="http://www.python.org/ftp/python/2.6.6/${PYTHON_MSI}"
    PYTHON_DIR="c:/Python26/"
    EASY_INSTALL="c:/Python26/Scripts/easy_install.exe"
    PIP="c:/Python26/Scripts/pip.exe"
    PYVERSION="cp26"
    TEMP_DIR="temp26"
elif [ "${TRAVIS_PYTHON_VERSION}" = "2.7" ]; then
    PYTHON_MSI="python-2.7.9${MSI_END}"
    PYTHON_URL="http://www.python.org/ftp/python/2.7.9/${PYTHON_MSI}"
    PYTHON_DIR="c:/Python27/"
    EASY_INSTALL="c:/Python27/Scripts/easy_install.exe"
    PIP="c:/Python27/Scripts/pip.exe"
    PYVERSION="cp27"
    TEMP_DIR="temp27"
elif [ "${TRAVIS_PYTHON_VERSION}" = "3.2" ]; then
    PYTHON_MSI="python-3.2.5${MSI_END}"
    PYTHON_URL="http://www.python.org/ftp/python/3.2.5/${PYTHON_MSI}"
    PYTHON_DIR="c:/Python32/"
    EASY_INSTALL="c:/Python32/Scripts/easy_install.exe"
    PIP="c:/Python32/Scripts/pip.exe"
    PYVERSION="cp32"
    TEMP_DIR="temp32"
elif [ "${TRAVIS_PYTHON_VERSION}" = "3.3" ]; then
    PYTHON_MSI="python-3.3.4${MSI_END}"
    PYTHON_URL="http://www.python.org/ftp/python/3.3.4/${PYTHON_MSI}"
    PYTHON_DIR="c:/Python33/"
    EASY_INSTALL="c:/Python33/Scripts/easy_install.exe"
    PIP="c:/Python33/Scripts/pip.exe"
    PYVERSION="cp33"
    TEMP_DIR="temp33"
elif [ "${TRAVIS_PYTHON_VERSION}" = "3.4" ]; then
    PYTHON_MSI="python-3.4.3${MSI_END}"
    PYTHON_URL="http://www.python.org/ftp/python/3.4.3/${PYTHON_MSI}"
    PYTHON_DIR="c:/Python34/"
    EASY_INSTALL="c:/Python34/Scripts/easy_install.exe"
    PIP="c:/Python34/Scripts/pip.exe"
    PYVERSION="cp34"
    TEMP_DIR="temp34"
else
    echo "Python ${TRAVIS_PYTHON_VERSION} not supported."
    exit 1;
fi

if [ "${BITS}" = "64" ]; then
    PYTHON="${PYTHON_DIR}python.exe"
    PYWIN32_EXE="pywin32-219.win-amd64-py${TRAVIS_PYTHON_VERSION}.exe"
    PYWIN32_URL="http://sourceforge.net/projects/pywin32/files/pywin32/Build%20219/${PYWIN32_EXE}/download"
    CFFI_WHEEL_URL="https://pypi.python.org/packages/${PYVERSION}/c/cffi/cffi-0.9.2-${PYVERSION}-none-win_amd64.whl"
    PYTHON_SITE_PACKAGES="${PYTHON_DIR}/lib/site-packages"
else
    PYTHON="${PYTHON_DIR}python.exe"
    PYWIN32_EXE="pywin32-219.win32-py${TRAVIS_PYTHON_VERSION}.exe"
    PYWIN32_URL="http://sourceforge.net/projects/pywin32/files/pywin32/Build%20219/${PYWIN32_EXE}/download"
    CFFI_WHEEL_URL="https://pypi.python.org/packages/${PYVERSION}/c/cffi/cffi-0.9.2-${PYVERSION}-none-win32.whl"
    PYTHON_SITE_PACKAGES="${PYTHON_DIR}/lib/site-packages"
fi


wget ${PYTHON_URL}
${WINE} msiexec /i ${PYTHON_MSI} /qn

wget https://pypi.python.org/packages/source/s/setuptools/setuptools-2.2.tar.gz
tar xf setuptools-2.2.tar.gz
(cd setuptools-2.2 && wine ${PYTHON} setup.py install)

wget ${PYWIN32_URL} -O ${PYWIN32_EXE}
zip -FFv ${PYWIN32_EXE} --out fixed.zip
unzip -o -qq fixed.zip -d ${TEMP_DIR}
${WINE} xcopy /R /E /Y /I  ${TEMP_DIR}/PLATLIB ${PYTHON_SITE_PACKAGES}
${WINE} ${PYTHON} ${TEMP_DIR}/SCRIPTS/pywin32_postinstall.py -install

if [ "${TRAVIS_PYTHON_VERSION}" = "2.6" ]; then
    wget https://pypi.python.org/packages/source/u/unittest2/unittest2-1.0.1.tar.gz#md5=6614a229aa3619e0d11542dd8f2fd8b8
    tar -xvf unittest2-1.0.1.tar.gz
    (cd unittest2-1.0.1 && ${WINE} ${PYTHON} setup.py install)
fi

wget https://pypi.python.org/packages/source/c/coverage/coverage-4.0a5.zip#md5=8a59799b1c1740d211346d6e88990815
unzip coverage-4.0a5.zip
(cd coverage-4.0a5 && wine ${PYTHON} setup.py install)

if [ "${CFFI}" = "true" ]; then
    ${WINE} ${EASY_INSTALL} pip
    ${WINE} ${PIP} install ${CFFI_WHEEL_URL}
fi

${WINE} ${PYTHON} setup.py install
