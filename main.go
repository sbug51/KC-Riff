package main

import (
	"context"

	"github.com/spf13/cobra"

	"github.com/sbug51/kcriff/cmd"
)

func main() {
	cobra.CheckErr(cmd.NewCLI().ExecuteContext(context.Background()))
}
