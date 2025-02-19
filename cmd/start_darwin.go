package cmd

import (
	"context"
	"errors"
	"os"
	"os/exec"
	"strings"

	"github.com/sbug51/kc-riff/api"
)

func startApp(ctx context.Context, client *api.Client) error {
	exe, err := os.Executable()
	if err != nil {
		return err
	}
	link, err := os.Readlink(exe)
	if err != nil {
		return err
	}
	if !strings.Contains(link, "kc-riff.app") {
		return errors.New("could not find kc-riff app")
	}
	path := strings.Split(link, "kc-riff.app")
	if err := exec.Command("/usr/bin/open", "-a", path[0]+"kc-riff.app").Run(); err != nil {
		return err
	}
	return waitForServer(ctx, client)
}
