package br.edu.ibmec.chatbot_api.controllers;

import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import br.edu.ibmec.chatbot_api.models.Cliente;
import br.edu.ibmec.chatbot_api.repository.ClienteRepository;

@RestController
@RequestMapping("/clientes")
public class ClientesController {
    // Métodos para lidar com requisições HTTP (GET, POST, PUT, DELETE) podem ser adicionados aqui
    @Autowired
    private ClienteRepository clienteRepository;

    @GetMapping
    public ResponseEntity<List<Cliente>> getClientes() {
        try {
            // Usa query personalizada para contornar problema do scanAvailable
            List<Cliente> clientes = clienteRepository.findAllClientes();

            // Log para debug
            System.out.println("📊 Total de clientes encontrados: " + clientes.size());
            for (int i = 0; i < clientes.size() && i < 3; i++) {
                Cliente c = clientes.get(i);
                System.out.println("Cliente " + i + ": " + c);
                System.out.println("  - ID: " + c.getId());
                System.out.println("  - Nome: " + c.getNome());
                System.out.println("  - Email: " + c.getEmail());
                System.out.println("  - CPF: " + c.getCpf());
            }

            return ResponseEntity.ok(clientes);
        } catch (Exception e) {
            System.err.println("❌ Erro ao buscar clientes: " + e.getMessage());
            e.printStackTrace();

            // Fallback para findAll() caso a query personalizada falhe
            List<Cliente> clientes = (List<Cliente>) clienteRepository.findAll();
            return ResponseEntity.ok(clientes);
        }
    }

    @GetMapping("/cpf/{cpf}")
    public ResponseEntity<Cliente> getClienteByCpf(@PathVariable String cpf) {
        Optional<Cliente> cliente = clienteRepository.findByCpf(cpf);

        if (cliente.isPresent()) {
            return ResponseEntity.ok(cliente.get());
        } else {
            return ResponseEntity.notFound().build();
        }
    }

    @PostMapping
    public ResponseEntity<Cliente> createCliente(@RequestBody Cliente cliente) {
        clienteRepository.save(cliente);
        return ResponseEntity.ok(cliente);
    }

    @PutMapping("/{id}")
    public ResponseEntity<Cliente> updateCliente(@PathVariable String id, @RequestBody Cliente cliente) {
        cliente.setId(id);
        clienteRepository.save(cliente);
        return ResponseEntity.ok(cliente);
    }

}
