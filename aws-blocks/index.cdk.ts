import * as cdk from 'aws-cdk-lib';
import { Hosting } from '@aws-blocks/blocks/cdk';
import { getStackName } from '@aws-blocks/blocks/scripts';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const __dirname = dirname(fileURLToPath(import.meta.url));

const app = new cdk.App();
cdk.Tags.of(app).add('aws-mcp:deploy:sop', 'migrate-static-site-to-blocks');
cdk.Tags.of(app).add('aws-mcp:deploy:launch-id', 'qeewmu70uqvrmkfchurk96ji');

const sandboxMode = app.node.tryGetContext('sandboxMode') === 'true';
const projectRoot = app.node.tryGetContext('projectRoot') || process.cwd();

// getStackName reads .blocks/config.json and suffixes -sandbox/-prod, so the
// scaffold's scripts target the same stack and sandbox never overwrites prod.
const stack = new cdk.Stack(app, getStackName({ sandbox: sandboxMode, projectRoot }), {
  // Make the deployment target explicit so the same project cannot silently
  // synthesize against whichever account or Region happens to be active.
  env: {
    account: process.env.CDK_DEFAULT_ACCOUNT,
    region: process.env.CDK_DEFAULT_REGION,
  },
});

// Hosting serves the pre-built static/ directory from S3 + CloudFront. Prod only.
// No buildCommand: the site is hand-written HTML committed in static/.
if (!sandboxMode) {
  new Hosting(stack, 'Hosting', {
    root: join(__dirname, '..'),
    framework: 'static',
    buildOutputDir: 'static',
    // This portfolio has no notification destination configured. Disable the
    // generated placeholder alarms instead of creating alarms that cannot
    // alert anyone. CloudFront/S3 service telemetry remains available in AWS.
    monitoring: { enabled: false },
  });
}
