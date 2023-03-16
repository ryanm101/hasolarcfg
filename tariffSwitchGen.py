# Requires pyaml
import sys
import yaml
import yaml.emitter
import yaml.serializer
import yaml.representer
import yaml.resolver


class IndentingEmitter(yaml.emitter.Emitter):
    def increase_indent(self, flow=False, indentless=False):
        """Ensure that lists items are always indented."""
        return super().increase_indent(
            flow=False,
            indentless=False,
        )


class PrettyDumper(
    IndentingEmitter,
    yaml.serializer.Serializer,
    yaml.representer.Representer,
    yaml.resolver.Resolver,
):
    def __init__(
        self,
        stream,
        default_style=None,
        default_flow_style=False,
        canonical=None,
        indent=None,
        width=None,
        allow_unicode=None,
        line_break=None,
        encoding=None,
        explicit_start=None,
        explicit_end=None,
        version=None,
        tags=None,
        sort_keys=True,
    ):
        IndentingEmitter.__init__(
            self,
            stream,
            canonical=canonical,
            indent=indent,
            width=width,
            allow_unicode=allow_unicode,
            line_break=line_break,
        )
        yaml.serializer.Serializer.__init__(
            self,
            encoding=encoding,
            explicit_start=explicit_start,
            explicit_end=explicit_end,
            version=version,
            tags=tags,
        )
        yaml.representer.Representer.__init__(
            self,
            default_style=default_style,
            default_flow_style=default_flow_style,
            sort_keys=sort_keys,
        )
        yaml.resolver.Resolver.__init__(self)


def main(args):
    utilfile = args[0]
    outfile = args[1]
    with open(utilfile,'r') as f:
        utility = yaml.safe_load(f)

    svc = []

    for i in utility['utility_meter'].keys():
        if 'tariffs' in utility['utility_meter'][i].keys():
            svcobj = dict(
                service="select.select_option",
                target=dict(
                    entity_id="select.{}".format(i)
                ),
                data=dict(
                    option="{{ tariff }}"
                )
            )

            svc.append(svcobj)
    x = dict(action=svc)

    with open(outfile,'a') as f:
        f.write(yaml.dump(x, Dumper=PrettyDumper))


if __name__ == "__main__":
    args = sys.argv[1:]
    main(args)
