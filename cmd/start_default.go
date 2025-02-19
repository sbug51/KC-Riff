//go:build !windows && !darwin

package cmd

import (
	"context"
	"errors"

	"github.com/sbug51/kcriff/api"
)

func startApp(ctx context.Context, client *api.Client) error {
	return errors.New("could not connect to kcriff server, run 'kcriff serve' to start it")
}
