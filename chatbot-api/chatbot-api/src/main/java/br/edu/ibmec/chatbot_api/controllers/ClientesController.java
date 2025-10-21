package br.edu.ibmec.chatbot_api.controllers;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;

import br.edu.ibmec.chatbot_api.models.Cliente;
import br.edu.ibmec.chatbot_api.repository.ClienteRepository;

@Controller
@RequestMapping("/clientes")
public class ClientesController {
    // Métodos para lidar com requisições HTTP (GET, POST, PUT, DELETE) podem ser adicionados aqui
    @Autowired
    private ClienteRepository clienteRepository;

    @GetMapping
    public ResponseEntity<Iterable<Cliente>> getClientes() {
        return ResponseEntity.ok(clienteRepository.findAll());
    }

    @PostMapping
    public ResponseEntity<Cliente> createCliente(@RequestBody Cliente cliente) {
        clienteRepository.save(cliente);
        return ResponseEntity.ok(cliente);
    }

    @PutMapping("/{id}")
    public ResponseEntity<Cliente> updateCliente(@PathVariable Long id, @RequestBody Cliente cliente) {
        cliente.setId(id);
        clienteRepository.save(cliente);
        return ResponseEntity.ok(cliente);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteCliente(@PathVariable Long id) {
        clienteRepository.deleteById(id);
        return ResponseEntity.noContent().build();
    }

}
