package br.edu.ibmec.chatbot_api.controllers;

import java.time.LocalDate;
import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import br.edu.ibmec.chatbot_api.models.ReservaHospedagem;
import br.edu.ibmec.chatbot_api.repository.ReservaHospedagemRepository;

@RestController
@RequestMapping("/api/reservas-hospedagem")
@CrossOrigin(origins = "*")
public class ReservaHospedagemController {

    @Autowired
    private ReservaHospedagemRepository reservaHospedagemRepository;

    // Listar todas as reservas de hospedagem
    @GetMapping
    public ResponseEntity<List<ReservaHospedagem>> getAllReservasHospedagem() {
        List<ReservaHospedagem> reservas = reservaHospedagemRepository.findAll();
        return ResponseEntity.ok(reservas);
    }

    // Buscar reserva por ID
    @GetMapping("/{id}")
    public ResponseEntity<ReservaHospedagem> getReservaHospedagemById(@PathVariable Long id) {
        Optional<ReservaHospedagem> reserva = reservaHospedagemRepository.findById(id);
        return reserva.map(ResponseEntity::ok)
                     .orElse(ResponseEntity.notFound().build());
    }

    // Criar nova reserva de hospedagem
    @PostMapping
    public ResponseEntity<ReservaHospedagem> createReservaHospedagem(@RequestBody ReservaHospedagem reservaHospedagem) {
        ReservaHospedagem savedReserva = reservaHospedagemRepository.save(reservaHospedagem);
        return ResponseEntity.ok(savedReserva);
    }

    // Atualizar reserva de hospedagem
    @PutMapping("/{id}")
    public ResponseEntity<ReservaHospedagem> updateReservaHospedagem(@PathVariable Long id, @RequestBody ReservaHospedagem reservaHospedagem) {
        if (!reservaHospedagemRepository.existsById(id)) {
            return ResponseEntity.notFound().build();
        }
        reservaHospedagem.setId(id);
        ReservaHospedagem updatedReserva = reservaHospedagemRepository.save(reservaHospedagem);
        return ResponseEntity.ok(updatedReserva);
    }

    // Deletar reserva de hospedagem
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteReservaHospedagem(@PathVariable Long id) {
        if (!reservaHospedagemRepository.existsById(id)) {
            return ResponseEntity.notFound().build();
        }
        reservaHospedagemRepository.deleteById(id);
        return ResponseEntity.noContent().build();
    }

    // Buscar reservas por cliente
    @GetMapping("/cliente/{clienteId}")
    public ResponseEntity<List<ReservaHospedagem>> getReservasByCliente(@PathVariable Long clienteId) {
        List<ReservaHospedagem> reservas = reservaHospedagemRepository.findByClienteId(clienteId);
        return ResponseEntity.ok(reservas);
    }

    // Buscar reservas por status
    @GetMapping("/status/{status}")
    public ResponseEntity<List<ReservaHospedagem>> getReservasByStatus(@PathVariable String status) {
        List<ReservaHospedagem> reservas = reservaHospedagemRepository.findByStatus(status);
        return ResponseEntity.ok(reservas);
    }

    // Buscar reservas por cliente e status
    @GetMapping("/cliente/{clienteId}/status/{status}")
    public ResponseEntity<List<ReservaHospedagem>> getReservasByClienteAndStatus(
            @PathVariable Long clienteId, @PathVariable String status) {
        List<ReservaHospedagem> reservas = reservaHospedagemRepository.findByClienteIdAndStatus(clienteId, status);
        return ResponseEntity.ok(reservas);
    }

    // Buscar hotéis por cidade
    @GetMapping("/cidade/{cidade}")
    public ResponseEntity<List<ReservaHospedagem>> getHoteisByCidade(@PathVariable String cidade) {
        List<ReservaHospedagem> reservas = reservaHospedagemRepository.findByCidadeContainingIgnoreCase(cidade);
        return ResponseEntity.ok(reservas);
    }

    // Buscar por nome do hotel
    @GetMapping("/hotel/{nomeHotel}")
    public ResponseEntity<List<ReservaHospedagem>> getReservasByHotel(@PathVariable String nomeHotel) {
        List<ReservaHospedagem> reservas = reservaHospedagemRepository.findByNomeHotelContainingIgnoreCase(nomeHotel);
        return ResponseEntity.ok(reservas);
    }

    // Buscar hotéis por cidade e nome
    @GetMapping("/buscar")
    public ResponseEntity<List<ReservaHospedagem>> getHoteisByCidadeAndNome(
            @RequestParam String cidade, @RequestParam String nomeHotel) {
        List<ReservaHospedagem> reservas = reservaHospedagemRepository
                .findByCidadeContainingIgnoreCaseAndNomeHotelContainingIgnoreCase(cidade, nomeHotel);
        return ResponseEntity.ok(reservas);
    }

    // Buscar por tipo de quarto
    @GetMapping("/tipo-quarto/{tipoQuarto}")
    public ResponseEntity<List<ReservaHospedagem>> getReservasByTipoQuarto(@PathVariable String tipoQuarto) {
        List<ReservaHospedagem> reservas = reservaHospedagemRepository.findByTipoQuartoContainingIgnoreCase(tipoQuarto);
        return ResponseEntity.ok(reservas);
    }

    // Buscar reservas por período de check-in
    @GetMapping("/periodo")
    public ResponseEntity<List<ReservaHospedagem>> getReservasByPeriodo(
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate dataInicio,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate dataFim) {
        List<ReservaHospedagem> reservas = reservaHospedagemRepository.findByDataCheckInBetween(dataInicio, dataFim);
        return ResponseEntity.ok(reservas);
    }

    // Buscar reservas ativas (hóspede está no hotel)
    @GetMapping("/ativas")
    public ResponseEntity<List<ReservaHospedagem>> getReservasAtivas() {
        LocalDate hoje = LocalDate.now();
        List<ReservaHospedagem> reservas = reservaHospedagemRepository.findReservasAtivas(hoje);
        return ResponseEntity.ok(reservas);
    }

    // Buscar reservas futuras de um cliente
    @GetMapping("/cliente/{clienteId}/futuras")
    public ResponseEntity<List<ReservaHospedagem>> getReservasFuturas(@PathVariable Long clienteId) {
        LocalDate hoje = LocalDate.now();
        List<ReservaHospedagem> reservas = reservaHospedagemRepository.findReservasFuturas(clienteId, hoje);
        return ResponseEntity.ok(reservas);
    }

    // Cancelar reserva (atualizar status)
    @PatchMapping("/{id}/cancelar")
    public ResponseEntity<ReservaHospedagem> cancelarReserva(@PathVariable Long id) {
        Optional<ReservaHospedagem> optionalReserva = reservaHospedagemRepository.findById(id);
        if (optionalReserva.isEmpty()) {
            return ResponseEntity.notFound().build();
        }
        
        ReservaHospedagem reserva = optionalReserva.get();
        reserva.setStatus("CANCELADA");
        ReservaHospedagem updatedReserva = reservaHospedagemRepository.save(reserva);
        return ResponseEntity.ok(updatedReserva);
    }
}