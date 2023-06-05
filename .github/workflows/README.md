# How do the workflows work?

1. When there is a push to the private repo's 'dev' branch (private/dev),
`regress` workflow runs the regression tests if the commit is not versioned.
`sync` workflow runs and makes sure that the versioned commit has a tag if it is
versioned. See [important notes](#important-notes) to see what "versioned
commit" means.

1. If `regress` workflow fails on 'private/dev', `sync` workflow gets triggered
and it pushes the latest changes to the public repo's 'dev' branch (public/dev).

1. If `regress` workflow successfully passes on 'private/dev', `version`
workflow gets triggered. It creates a new version commit and tag, and pushes to
'private/dev', 'public/dev', and 'public/stable'.

1. When there is a push with new version to the 'public/stable' branch, `deploy`
workflow runs. It deploys the PyPI package of OpenRAM and creates a new GitHub
release on that repo.



## Important Notes

1. Workflows understand that the latest commit is versioned  with the following
commit message syntax.

    ```
    Bump version: <any message>
    ```

    Automatically generated version commits have the following syntax:

    ```
    Bump version: a.b.c -> a.b.d
    ```

1. `version` workflow only increments the right-most version digit. Other digits
in the version number must be updated manually, following the syntax above. Just
following this syntax is enough for workflows to create a new version
automatically. That means, you don't have to tag that commit manually.

1. `regress` workflow doesn't run if the push has a new version. We assume that
this commit was automatically generated after a previous commit passed `regress`
workflow or was manually generated with caution.

1. `regress` workflow doesn't run on the public repo.

1. `deploy` workflow only runs on branches named 'stable'.

1. `version` workflow is only triggered from branches named 'dev' if they pass
`regress` workflow.

1. `sync` workflow only runs on the private repo.

1. `sync_tag` workflow only runs on the private repo.

1. Merging pull requests on the private repo should be safe in any case. They
are treated the same as commit pushes.

> **Warning**: `regress` workflow is currently disabled on the public repo
> manually. This was done because of a security risk on our private server.
> Enabling it on GitHub will run `regress` workflow on the public repo.


## Flowchart
```mermaid
flowchart TD

start((Start));
privatedev[(PrivateRAM/dev)];
publicdev[(OpenRAM/dev)];
publicstable[(OpenRAM/stable)];
regressprivate{{regress}};
regresspublic{{regress}};
syncnover{{sync}};
synctag{{sync_tag}};
deploy{{deploy}};
versionprivate{{version}};
versionpublic{{version}};

privateif1(Is versioned?);
privateif2(Has version tag?);
privateif3(Did tests pass?);

publicif1(Is versioned?);
publicif2(Is versioned?);
publicif3(Did tests pass?)

start-- Push commit -->privatedev
    privatedev-->privateif1
    privateif1-- Yes -->privateif2
        privateif2-- No -->synctag
    privateif1-- No -->regressprivate
        regressprivate-->privateif3
            privateif3-- Yes -->versionprivate
            privateif3-- No -->syncnover

start-- Push commit / Merge PR -->publicdev
publicdev-->publicif1
    publicif1-- No -->regresspublic
        regresspublic-->publicif3
            publicif3-- Yes -->versionpublic

start-- "Push commit (from workflows)" -->publicstable
publicstable-->publicif2
    publicif2-- Yes -->deploy
```

