package br.edu.ibmec.chatbot_api.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import br.edu.ibmec.chatbot_api.models.ReservaVoo;

import java.time.LocalDateTime;
import java.util.List;

@Repository
public interface ReservaVooRepository extends JpaRepository<ReservaVoo, Long> {
    
    // Buscar todas as reservas de um cliente específico
    List<ReservaVoo> findByClienteId(Long clienteId);
    
    // Buscar reservas por status
    List<ReservaVoo> findByStatus(String status);
    
    // Buscar reservas de um cliente por status
    List<ReservaVoo> findByClienteIdAndStatus(Long clienteId, String status);
    
    // Buscar voos por origem
    List<ReservaVoo> findByOrigemContainingIgnoreCase(String origem);
    
    // Buscar voos por destino
    List<ReservaVoo> findByDestinoContainingIgnoreCase(String destino);
    
    // Buscar voos por origem e destino
    List<ReservaVoo> findByOrigemContainingIgnoreCaseAndDestinoContainingIgnoreCase(String origem, String destino);
    
    // Buscar voos por companhia aérea
    List<ReservaVoo> findByCompanhiaAereaContainingIgnoreCase(String companhiaAerea);
    
    // Buscar voos por período de partida
    @Query("SELECT r FROM ReservaVoo r WHERE r.dataHoraPartida BETWEEN :dataInicio AND :dataFim")
    List<ReservaVoo> findByDataHoraPartidaBetween(@Param("dataInicio") LocalDateTime dataInicio, 
                                                   @Param("dataFim") LocalDateTime dataFim);
    
    // Buscar voos por cliente e período
    @Query("SELECT r FROM ReservaVoo r WHERE r.clienteId = :clienteId AND r.dataHoraPartida BETWEEN :dataInicio AND :dataFim")
    List<ReservaVoo> findByClienteIdAndDataHoraPartidaBetween(@Param("clienteId") Long clienteId,
                                                              @Param("dataInicio") LocalDateTime dataInicio,
                                                              @Param("dataFim") LocalDateTime dataFim);
}