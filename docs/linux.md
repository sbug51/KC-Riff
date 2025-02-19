# Linux

## Install

To install kc-riff, run the following command:

```shell
# curl -fsSL https://kc-riff.com/install.sh | sh
```

## Manual install

> [!NOTE]
> If you are upgrading from a prior version, you should remove the old libraries with `sudo rm -rf /usr/lib/kc-riff` first.

Download and extract the package:

```shell
# curl -L https://kc-riff.com/download/kc-riff-linux-amd64.tgz -o kc-riff-linux-amd64.tgz
sudo tar -C /usr -xzf kc-riff-linux-amd64.tgz
```

Start kc-riff:

```shell
kc-riff serve
```

In another terminal, verify that kc-riff is running:

```shell
kc-riff -v
```

### AMD GPU install

If you have an AMD GPU, also download and extract the additional ROCm package:

```shell
# curl -L https://kc-riff.com/download/kc-riff-linux-amd64-rocm.tgz -o kc-riff-linux-amd64-rocm.tgz
sudo tar -C /usr -xzf kc-riff-linux-amd64-rocm.tgz
```

### ARM64 install

Download and extract the ARM64-specific package:

```shell
# curl -L https://kc-riff.com/download/kc-riff-linux-arm64.tgz -o kc-riff-linux-arm64.tgz
sudo tar -C /usr -xzf kc-riff-linux-arm64.tgz
```

### Adding kc-riff as a startup service (recommended)

Create a user and group for kc-riff:

```shell
sudo useradd -r -s /bin/false -U -m -d /usr/share/kc-riff kc-riff
sudo usermod -a -G kc-riff $(whoami)
```

Create a service file in `/etc/systemd/system/kc-riff.service`:

```ini
[Unit]
Description=kc-riff Service
After=network-online.target

[Service]
ExecStart=/usr/bin/kc-riff serve
User=kc-riff
Group=kc-riff
Restart=always
RestartSec=3
Environment="PATH=$PATH"

[Install]
WantedBy=default.target
```

Then start the service:

```shell
sudo systemctl daemon-reload
sudo systemctl enable kc-riff
```

### Install CUDA drivers (optional)

[Download and install](https://developer.nvidia.com/cuda-downloads) CUDA.

Verify that the drivers are installed by running the following command, which should print details about your GPU:

```shell
nvidia-smi
```

### Install AMD ROCm drivers (optional)

[Download and Install](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/tutorial/quick-start.html) ROCm v6.

### Start kc-riff

Start kc-riff and verify it is running:

```shell
sudo systemctl start kc-riff
sudo systemctl status kc-riff
```

> [!NOTE]
> While AMD has contributed the `amdgpu` driver upstream to the official linux
> kernel source, the version is older and may not support all ROCm features. We
> recommend you install the latest driver from
> https://www.amd.com/en/support/linux-drivers for best support of your Radeon
> GPU.

## Customizing

To customize the installation of kc-riff, you can edit the systemd service file or the environment variables by running:

```shell
sudo systemctl edit kc-riff
```

Alternatively, create an override file manually in `/etc/systemd/system/kc-riff.service.d/override.conf`:

```ini
[Service]
Environment="OLLAMA_DEBUG=1"
```

## Updating

Update kc-riff by running the install script again:

```shell
# curl -fsSL https://kc-riff.com/install.sh | sh
```

Or by re-downloading kc-riff:

```shell
# curl -L https://kc-riff.com/download/kc-riff-linux-amd64.tgz -o kc-riff-linux-amd64.tgz
sudo tar -C /usr -xzf kc-riff-linux-amd64.tgz
```

## Installing specific versions

Use `OLLAMA_VERSION` environment variable with the install script to install a specific version of kc-riff, including pre-releases. You can find the version numbers in the [releases page](https://github.com/sbug51/kc-riff/releases).

For example:

```shell
# curl -fsSL https://kc-riff.com/install.sh | OLLAMA_VERSION=0.5.7 sh
```

## Viewing logs

To view logs of kc-riff running as a startup service, run:

```shell
journalctl -e -u kc-riff
```

## Uninstall

Remove the kc-riff service:

```shell
sudo systemctl stop kc-riff
sudo systemctl disable kc-riff
sudo rm /etc/systemd/system/kc-riff.service
```

Remove the kc-riff binary from your bin directory (either `/usr/local/bin`, `/usr/bin`, or `/bin`):

```shell
sudo rm $(which kc-riff)
```

Remove the downloaded models and kc-riff service user and group:

```shell
sudo rm -r /usr/share/kc-riff
sudo userdel kc-riff
sudo groupdel kc-riff
```

Remove installed libraries:

```shell
sudo rm -rf /usr/local/lib/kc-riff
```
