# Linux

## Install

To install kcriff, run the following command:

```shell
# curl -fsSL https://kcriff.com/install.sh | sh
```

## Manual install

> [!NOTE]
> If you are upgrading from a prior version, you should remove the old libraries with `sudo rm -rf /usr/lib/kcriff` first.

Download and extract the package:

```shell
# curl -L https://kcriff.com/download/kcriff-linux-amd64.tgz -o kcriff-linux-amd64.tgz
sudo tar -C /usr -xzf kcriff-linux-amd64.tgz
```

Start kcriff:

```shell
kcriff serve
```

In another terminal, verify that kcriff is running:

```shell
kcriff -v
```

### AMD GPU install

If you have an AMD GPU, also download and extract the additional ROCm package:

```shell
# curl -L https://kcriff.com/download/kcriff-linux-amd64-rocm.tgz -o kcriff-linux-amd64-rocm.tgz
sudo tar -C /usr -xzf kcriff-linux-amd64-rocm.tgz
```

### ARM64 install

Download and extract the ARM64-specific package:

```shell
# curl -L https://kcriff.com/download/kcriff-linux-arm64.tgz -o kcriff-linux-arm64.tgz
sudo tar -C /usr -xzf kcriff-linux-arm64.tgz
```

### Adding kcriff as a startup service (recommended)

Create a user and group for kcriff:

```shell
sudo useradd -r -s /bin/false -U -m -d /usr/share/kcriff kcriff
sudo usermod -a -G kcriff $(whoami)
```

Create a service file in `/etc/systemd/system/kcriff.service`:

```ini
[Unit]
Description=kcriff Service
After=network-online.target

[Service]
ExecStart=/usr/bin/kcriff serve
User=kcriff
Group=kcriff
Restart=always
RestartSec=3
Environment="PATH=$PATH"

[Install]
WantedBy=default.target
```

Then start the service:

```shell
sudo systemctl daemon-reload
sudo systemctl enable kcriff
```

### Install CUDA drivers (optional)

[Download and install](https://developer.nvidia.com/cuda-downloads) CUDA.

Verify that the drivers are installed by running the following command, which should print details about your GPU:

```shell
nvidia-smi
```

### Install AMD ROCm drivers (optional)

[Download and Install](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/tutorial/quick-start.html) ROCm v6.

### Start kcriff

Start kcriff and verify it is running:

```shell
sudo systemctl start kcriff
sudo systemctl status kcriff
```

> [!NOTE]
> While AMD has contributed the `amdgpu` driver upstream to the official linux
> kernel source, the version is older and may not support all ROCm features. We
> recommend you install the latest driver from
> https://www.amd.com/en/support/linux-drivers for best support of your Radeon
> GPU.

## Customizing

To customize the installation of kcriff, you can edit the systemd service file or the environment variables by running:

```shell
sudo systemctl edit kcriff
```

Alternatively, create an override file manually in `/etc/systemd/system/kcriff.service.d/override.conf`:

```ini
[Service]
Environment="kcRiff_DEBUG=1"
```

## Updating

Update kcriff by running the install script again:

```shell
# curl -fsSL https://kcriff.com/install.sh | sh
```

Or by re-downloading kcriff:

```shell
# curl -L https://kcriff.com/download/kcriff-linux-amd64.tgz -o kcriff-linux-amd64.tgz
sudo tar -C /usr -xzf kcriff-linux-amd64.tgz
```

## Installing specific versions

Use `kcRiff_VERSION` environment variable with the install script to install a specific version of kcriff, including pre-releases. You can find the version numbers in the [releases page](https://github.com/sbug51/kcriff/releases).

For example:

```shell
# curl -fsSL https://kcriff.com/install.sh | kcRiff_VERSION=0.5.7 sh
```

## Viewing logs

To view logs of kcriff running as a startup service, run:

```shell
journalctl -e -u kcriff
```

## Uninstall

Remove the kcriff service:

```shell
sudo systemctl stop kcriff
sudo systemctl disable kcriff
sudo rm /etc/systemd/system/kcriff.service
```

Remove the kcriff binary from your bin directory (either `/usr/local/bin`, `/usr/bin`, or `/bin`):

```shell
sudo rm $(which kcriff)
```

Remove the downloaded models and kcriff service user and group:

```shell
sudo rm -r /usr/share/kcriff
sudo userdel kcriff
sudo groupdel kcriff
```

Remove installed libraries:

```shell
sudo rm -rf /usr/local/lib/kcriff
```
