# How to write an importer
Importers currently support the importing functionality for finding templates.

## Copy an existing importer
You can copy, for example, the Ghostwriter plugin, either to the project, or to `.sysreptor/plugins` in your home directory.

Rename the `Ghostwriter` directory and `Ghostwriter.py` to the same name. Also update the `loader` variable at the bottom to your new class.

You will be able to call your plugin via `reptor <plugin name in lowercase>`.

TODO: In the future, we want to provide an empty boilerplate that is copied automatically.

## Importer settings

You will have to use some settings in your plugin, like from what URL the data should be fetched, or the API key. There are two options how to provide those settings:

* CLI parameter
* config.yaml

### Settings via CLI parameter

Use the `add_arguments` method to add your custom CLI arguments

```python
    @classmethod
    def add_arguments(cls, parser, plugin_filepath=None):
        super().add_arguments(parser, plugin_filepath)
        action_group = parser.add_argument_group()
        action_group.add_argument(
            "-url",
            "--url",
            metavar="URL",
            action="store",
            const="",
            nargs="?",
            help="API Url",
        )
```

You can use `--help` to check if your arguments are available: `reptor <your plugin name> --help`.

Access your arguments via the `kwargs` dictionary in `__init__.py`, e. g. `self.url = kwargs.get("url", "")`

### Settings via config.yaml

reptor settings are managed in `.sysreptor/config.yaml` in your home directory. You can add plugin specific settings there, e. g.:

```yaml
community: true
private_note: false
project_id: 42c2f73a-4383-4ec2-a3fa-281598edb0e8
server: https://demo.sysre.pt
token: sysreptor_TOKEN

your_plugin:
  apikey: your_api_key
  url: http://localhost:8080
```

Those settings are attributes of `self` in your plugin. If those settings are mandatory, you can raise an exception if they are not present, e. g.:

```python
if not hasattr(self, "apikey"):
    raise ValueError(
        "API Key is required. Add to your user config."
    )
```

## Fetch finding templates from source

It's time to get findings from your source. Use the `next_findings_batch` method to yield finding template by finding template, e. g.:

```python
    def next_findings_batch(self):
        findings = self._get_findings_from_source()
        for finding_data in findings:
            yield finding_data
```

Note that you have to implement `_get_findings_from_source`. This is where you access your source's API.

`finding_data` is a dictionary containing the fields of your source, e. g.:

```json
{
    "title": "Finding Title",
	"description": "Finding Description",
    "links": "https://example.com/\nhttps://example.com/reference"
}
```

The field names should be those from your source, not from SysReptor.

## Mapping field names

Define a `mapping` attribute in your class to map the field names of your source to the SysReptor fields, e. g.:

```json
{
    "title": "title",
	"description": "description",
    "links": "references"
}
```

In this example, the source field `title` maps to the SysReptor field `title`. However, the source field `links` should be mapped to the field `references`.

We encourage you to map to predefined SysReptor fields only. This guarantees compatibility with all SysReptor installations.

## Processing values

In the example above, the `links` field containes a newline-separated field of links. However, `references` in SysReptor is a list. To process and/or convert values, you can define a method called `convert_<source field name>`. This will be called to preprocess the values of the fields.

```python
    def convert_links(self, value):
        return value.splitlines()
```