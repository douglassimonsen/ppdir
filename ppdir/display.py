from colorama import Fore, Style, init

init()


def _display(
    data: dict[str, Categories],
    *,
    class_order: list[str],
    include_dunders: bool = False,
    include_docs: bool = True,
) -> None:
    # We reverse the class order so the most specific class is on the bottom since that's likely what people care about
    for class_name in class_order[::-1]:
        print(f"\n{Fore.BLUE}{class_name}{Style.RESET_ALL}")
        vals = data.get(class_name, Categories())
        if vals.attributes:
            print("    Attributes:")
            max_len = max(len(val.name) for val in vals.attributes)
            for val in vals.attributes:
                val_str = val.to_string(include_docs=include_docs, max_len=max_len)
                print(
                    f"        {Fore.GREEN}{val_str}{Style.RESET_ALL}",
                )
        if vals.methods:
            print("    Methods:")
            max_len = max(len(val.name) for val in vals.methods)
            for val in vals.methods:
                val_str = val.to_string(include_docs=include_docs, max_len=max_len)
                print(
                    f"        {Fore.YELLOW}{val_str}{Style.RESET_ALL}",
                )
        if vals.dunders and include_dunders:
            print("    Dunders:")
            max_len = max(len(val.name) for val in vals.dunders)
            for val in vals.dunders:
                val_str = val.to_string(include_docs=include_docs, max_len=max_len)
                print(f"        {Fore.RED}{val_str}{Style.RESET_ALL}")
