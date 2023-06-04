import math
from Ma3yTuKserializer.serializers.json_serializer import Json
from Ma3yTuKserializer.serializers.xml_serializer import Xml


def main():
    serializer = Json()
    serializer.dumps("Hello")


if __name__ == "__main__":
    main()
