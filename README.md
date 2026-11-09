# Paper to Research GIF

A portable Codex skill for turning a scientific paper into a source-grounded, approximately five-second animated GIF. The GIF shows one research mechanism or carefully qualified result at a glance; it is not a compressed slide deck or a claim that an illustrative animation is measured footage.

## Install in a Codex repository

```text
git clone https://github.com/Jihoon950/paper-to-research-gif.git
cd paper-to-research-gif
python scripts/install_repo_skill.py <your-repository-directory>
```

In that repository, ask Codex: `Use $paper-to-research-gif to make a five-second GIF that explains this paper.` Supply the paper PDF or URL and any approved visual assets. The skill makes a paper-specific shot map, animation source, GIF, representative still, source ledger, and alt text. GIF encoding uses Python and Pillow; the agent may use a code-native scene renderer that fits the paper.

## Portable package

```text
python scripts/package_release.py --output paper-to-research-gif-0.1.0.zip
```

The package contains the plugin manifest, icon, skill, and GIF encoder. It does not contain research papers, private drafts, institutional logos, or example media. Actual paper GIFs belong in the user's production folder.

The encoder verifies frame dimensions, approximately five-second duration, infinite loop metadata, and file size. It does not establish the scientific accuracy of a GIF; check each visual statement against the paper. See the [official plugin package guide](https://developers.openai.com/plugins/build/plugins) for the package structure.
