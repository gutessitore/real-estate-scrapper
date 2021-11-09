driver = init_driver()
site = "https://www.google.com/"
address = "R. Monte Alegre"
driver.get(site)

# your code

driver.close()

output_json = [
  {"valor": 123, "endereço": "abc", "vagas": 123, "valor_de_condominio": 123, "tamanho": 123, "quartos": 123, "banheiros": 123},
  {"valor": 123, "endereço": "abc", "vagas": 123, "valor_de_condominio": 123, "tamanho": 123, "quartos": 123, "banheiros": 123}
]

output_filename = build_output_filename(site, address)
save_raw_data(output_json, output_filename)
