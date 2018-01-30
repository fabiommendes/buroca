from invoke import task


@task(
    help={'part': 'semver part (major, minor or patch)'}
)
def bump_version(ctx, part='patch'):
    "Bumps package version according to semantic versioning."

    if part not in {'patch', 'major', 'minor'}:
        msg = 'invalid part: %r. Must be either patch, major or minor.' % part
        raise SystemExit(msg)
    
    ctx.run('bumpversion --config-file bumpversion.cfg %s' % part)
