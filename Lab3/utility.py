from Ma3yTuKserializer.serializers.serializer_factory import SerializerFactory
import typer


app = typer.Typer()


@app.command()
def serializer(file_from: str,file_to:str,format_from:str,format_to:str):
    ser_from = SerializerFactory.get_serializer(format_from)
    ser_to=SerializerFactory.get_serializer(format_to)
    with open(file_from,'r') as rf, open (file_to,'w') as ft:
        temp_res = ser_from.load(rf)
        print(temp_res)
        ser_to.dump(temp_res,ft) 


if __name__ == "__main__":
    app()