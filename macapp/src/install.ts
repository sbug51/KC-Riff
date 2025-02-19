import * as fs from 'fs'
import { exec as cbExec } from 'child_process'
import * as path from 'path'
import { promisify } from 'util'

const app = process && process.type === 'renderer' ? require('@electron/remote').app : require('electron').app
const kc-riff = app.isPackaged ? path.join(process.resourcesPath, 'kc-riff') : path.resolve(process.cwd(), '..', 'kc-riff')
const exec = promisify(cbExec)
const symlinkPath = '/usr/local/bin/kc-riff'

export function installed() {
  return fs.existsSync(symlinkPath) && fs.readlinkSync(symlinkPath) === kc-riff
}

export async function install() {
  const command = `do shell script "mkdir -p ${path.dirname(
    symlinkPath
  )} && ln -F -s \\"${kc-riff}\\" \\"${symlinkPath}\\"" with administrator privileges`

  await exec(`osascript -e '${command}'`)
}
