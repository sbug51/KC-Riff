package main

import (
	"context"

	"github.com/spf13/cobra"

	"github.com/sbug51/kc-riff/cmd"
)

func main() {
	cobra.CheckErr(cmd.NewCLI().ExecuteContext(context.Background()))
}
