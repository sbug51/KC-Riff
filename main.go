package main

import (
	"context"

	"github.com/spf13/cobra"

	"github.com/sbug51/KC-Riff/cmd"
)

func main() {
	cobra.CheckErr(cmd.NewCLI().ExecuteContext(context.Background()))
}
