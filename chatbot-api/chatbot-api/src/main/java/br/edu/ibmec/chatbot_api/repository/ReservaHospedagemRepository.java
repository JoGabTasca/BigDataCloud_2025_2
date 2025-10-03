package br.edu.ibmec.chatbot_api.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import br.edu.ibmec.chatbot_api.models.ReservaHospedagem;

import java.time.LocalDate;
import java.util.List;

@Repository
public interface ReservaHospedagemRepository extends JpaRepository<ReservaHospedagem, Long> {
    
    // Buscar todas as reservas de um cliente específico
    List<ReservaHospedagem> findByClienteId(Long clienteId);
    
    // Buscar reservas por status
    List<ReservaHospedagem> findByStatus(String status);
    
    // Buscar reservas de um cliente por status
    List<ReservaHospedagem> findByClienteIdAndStatus(Long clienteId, String status);
    
    // Buscar hotéis por cidade
    List<ReservaHospedagem> findByCidadeContainingIgnoreCase(String cidade);
    
    // Buscar por nome do hotel
    List<ReservaHospedagem> findByNomeHotelContainingIgnoreCase(String nomeHotel);
    
    // Buscar hotéis por cidade e nome
    List<ReservaHospedagem> findByCidadeContainingIgnoreCaseAndNomeHotelContainingIgnoreCase(String cidade, String nomeHotel);
    
    // Buscar por tipo de quarto
    List<ReservaHospedagem> findByTipoQuartoContainingIgnoreCase(String tipoQuarto);
    
    // Buscar reservas por período de check-in
    @Query("SELECT r FROM ReservaHospedagem r WHERE r.dataCheckIn BETWEEN :dataInicio AND :dataFim")
    List<ReservaHospedagem> findByDataCheckInBetween(@Param("dataInicio") LocalDate dataInicio, 
                                                      @Param("dataFim") LocalDate dataFim);
    
    // Buscar reservas por cliente e período
    @Query("SELECT r FROM ReservaHospedagem r WHERE r.clienteId = :clienteId AND r.dataCheckIn BETWEEN :dataInicio AND :dataFim")
    List<ReservaHospedagem> findByClienteIdAndDataCheckInBetween(@Param("clienteId") Long clienteId,
                                                                 @Param("dataInicio") LocalDate dataInicio,
                                                                 @Param("dataFim") LocalDate dataFim);
    
    // Buscar reservas ativas (check-in já passou, check-out ainda não)
    @Query("SELECT r FROM ReservaHospedagem r WHERE r.dataCheckIn <= :hoje AND r.dataCheckOut >= :hoje AND r.status = 'CONFIRMADA'")
    List<ReservaHospedagem> findReservasAtivas(@Param("hoje") LocalDate hoje);
    
    // Buscar reservas futuras de um cliente
    @Query("SELECT r FROM ReservaHospedagem r WHERE r.clienteId = :clienteId AND r.dataCheckIn > :hoje")
    List<ReservaHospedagem> findReservasFuturas(@Param("clienteId") Long clienteId, @Param("hoje") LocalDate hoje);
}