import person_pb2  # Arquivo gerado pelo protoc

# Criar uma instância de Person
person = person_pb2.Person()
person.name = "Alice"
person.id = 1234
person.email = "alice@example.com"

# Serializar
serialized_data = person.SerializeToString()
print(f"Serialized data: {serialized_data}")

# Desserializar
new_person = person_pb2.Person()
new_person.ParseFromString(serialized_data)

# Exibir os dados desserializados
print("\nDeserialized data:")
print(f"Name: {new_person.name}")
print(f"ID: {new_person.id}")
print(f"Email: {new_person.email}")
