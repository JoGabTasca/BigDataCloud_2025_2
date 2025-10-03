package br.edu.ibmec.chatbot_api.controllers;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import br.edu.ibmec.chatbot_api.models.ReservaVoo;
import br.edu.ibmec.chatbot_api.repository.ReservaVooRepository;

@RestController
@RequestMapping("/api/reservas-voo")
@CrossOrigin(origins = "*")
public class ReservaVooController {

    @Autowired
    private ReservaVooRepository reservaVooRepository;

    // Listar todas as reservas de voo
    @GetMapping
    public ResponseEntity<List<ReservaVoo>> getAllReservasVoo() {
        List<ReservaVoo> reservas = reservaVooRepository.findAll();
        return ResponseEntity.ok(reservas);
    }

    // Buscar reserva por ID
    @GetMapping("/{id}")
    public ResponseEntity<ReservaVoo> getReservaVooById(@PathVariable Long id) {
        Optional<ReservaVoo> reserva = reservaVooRepository.findById(id);
        return reserva.map(ResponseEntity::ok)
                     .orElse(ResponseEntity.notFound().build());
    }

    // Criar nova reserva de voo
    @PostMapping
    public ResponseEntity<ReservaVoo> createReservaVoo(@RequestBody ReservaVoo reservaVoo) {
        ReservaVoo savedReserva = reservaVooRepository.save(reservaVoo);
        return ResponseEntity.ok(savedReserva);
    }

    // Atualizar reserva de voo
    @PutMapping("/{id}")
    public ResponseEntity<ReservaVoo> updateReservaVoo(@PathVariable Long id, @RequestBody ReservaVoo reservaVoo) {
        if (!reservaVooRepository.existsById(id)) {
            return ResponseEntity.notFound().build();
        }
        reservaVoo.setId(id);
        ReservaVoo updatedReserva = reservaVooRepository.save(reservaVoo);
        return ResponseEntity.ok(updatedReserva);
    }

    // Deletar reserva de voo
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteReservaVoo(@PathVariable Long id) {
        if (!reservaVooRepository.existsById(id)) {
            return ResponseEntity.notFound().build();
        }
        reservaVooRepository.deleteById(id);
        return ResponseEntity.noContent().build();
    }

    // Buscar reservas por cliente
    @GetMapping("/cliente/{clienteId}")
    public ResponseEntity<List<ReservaVoo>> getReservasByCliente(@PathVariable Long clienteId) {
        List<ReservaVoo> reservas = reservaVooRepository.findByClienteId(clienteId);
        return ResponseEntity.ok(reservas);
    }

    // Buscar reservas por status
    @GetMapping("/status/{status}")
    public ResponseEntity<List<ReservaVoo>> getReservasByStatus(@PathVariable String status) {
        List<ReservaVoo> reservas = reservaVooRepository.findByStatus(status);
        return ResponseEntity.ok(reservas);
    }

    // Buscar reservas por cliente e status
    @GetMapping("/cliente/{clienteId}/status/{status}")
    public ResponseEntity<List<ReservaVoo>> getReservasByClienteAndStatus(
            @PathVariable Long clienteId, @PathVariable String status) {
        List<ReservaVoo> reservas = reservaVooRepository.findByClienteIdAndStatus(clienteId, status);
        return ResponseEntity.ok(reservas);
    }

    // Buscar voos por origem
    @GetMapping("/origem/{origem}")
    public ResponseEntity<List<ReservaVoo>> getVoosByOrigem(@PathVariable String origem) {
        List<ReservaVoo> reservas = reservaVooRepository.findByOrigemContainingIgnoreCase(origem);
        return ResponseEntity.ok(reservas);
    }

    // Buscar voos por destino
    @GetMapping("/destino/{destino}")
    public ResponseEntity<List<ReservaVoo>> getVoosByDestino(@PathVariable String destino) {
        List<ReservaVoo> reservas = reservaVooRepository.findByDestinoContainingIgnoreCase(destino);
        return ResponseEntity.ok(reservas);
    }

    // Buscar voos por origem e destino
    @GetMapping("/rota")
    public ResponseEntity<List<ReservaVoo>> getVoosByRota(
            @RequestParam String origem, @RequestParam String destino) {
        List<ReservaVoo> reservas = reservaVooRepository
                .findByOrigemContainingIgnoreCaseAndDestinoContainingIgnoreCase(origem, destino);
        return ResponseEntity.ok(reservas);
    }

    // Buscar voos por companhia aérea
    @GetMapping("/companhia/{companhia}")
    public ResponseEntity<List<ReservaVoo>> getVoosByCompanhia(@PathVariable String companhia) {
        List<ReservaVoo> reservas = reservaVooRepository.findByCompanhiaAereaContainingIgnoreCase(companhia);
        return ResponseEntity.ok(reservas);
    }

    // Buscar voos por período
    @GetMapping("/periodo")
    public ResponseEntity<List<ReservaVoo>> getVoosByPeriodo(
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE_TIME) LocalDateTime dataInicio,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE_TIME) LocalDateTime dataFim) {
        List<ReservaVoo> reservas = reservaVooRepository.findByDataHoraPartidaBetween(dataInicio, dataFim);
        return ResponseEntity.ok(reservas);
    }

    // Cancelar reserva (atualizar status)
    @PatchMapping("/{id}/cancelar")
    public ResponseEntity<ReservaVoo> cancelarReserva(@PathVariable Long id) {
        Optional<ReservaVoo> optionalReserva = reservaVooRepository.findById(id);
        if (optionalReserva.isEmpty()) {
            return ResponseEntity.notFound().build();
        }
        
        ReservaVoo reserva = optionalReserva.get();
        reserva.setStatus("CANCELADA");
        ReservaVoo updatedReserva = reservaVooRepository.save(reserva);
        return ResponseEntity.ok(updatedReserva);
    }
}