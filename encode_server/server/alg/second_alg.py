    def process_file(alg_name: str, data: bytes, encode: bool = True) -> io.BytesIO:
    logger.info(f"Importing module {module_name}")
    module_name = f"alg.{alg_name}"
    if module_name in sys.modules:
        module = sys.modules[module_name]
    else:
        module =  importlib.import_module(module_name)
    if ("encode" not in module.__dir__) or ("decode" not in module.__dir__):
        raise ImportError("Модуль не содержит нужных функций")
    logger.info(f"Coding data")
    if encode:
        output = module.encode(data)
    else:
        output = module.decode(data)
    logger.info(f"Encoded data length: {len(output)}")
    return io.BytesIO(output)