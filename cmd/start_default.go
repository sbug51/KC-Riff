//go:build !windows && !darwin

package cmd

import (
	"context"
	"errors"

	"github.com/sbug51/kc-riff/api"
)

func startApp(ctx context.Context, client *api.Client) error {
	return errors.New("could not connect to kc-riff server, run 'kc-riff serve' to start it")
}
