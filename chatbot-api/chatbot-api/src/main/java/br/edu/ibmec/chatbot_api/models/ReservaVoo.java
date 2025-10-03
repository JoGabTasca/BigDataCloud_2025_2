package br.edu.ibmec.chatbot_api.models;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Entity
@Table(name = "reserva_voo")
public class ReservaVoo {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false)
    private Long clienteId;
    
    @Column(nullable = false, length = 100)
    private String origem;
    
    @Column(nullable = false, length = 100)
    private String destino;
    
    @Column(nullable = false)
    private LocalDateTime dataHoraPartida;
    
    @Column(nullable = true)
    private LocalDateTime dataHoraChegada;
    
    @Column(nullable = true)
    private LocalDateTime dataHoraVolta;
    
    @Column(nullable = false, length = 100)
    private String companhiaAerea;
    
    @Column(nullable = false, length = 20)
    private String numeroVoo;
    
    @Column(length = 10)
    private String assento;
    
    @Column(length = 50)
    private String classe; // ECONOMICA, EXECUTIVA, PRIMEIRA_CLASSE
    
    @Column(nullable = false, precision = 10, scale = 2)
    private BigDecimal preco;
    
    @Column(nullable = false, length = 50)
    private String status; // CONFIRMADA, CANCELADA, PENDENTE
    
    @Column(length = 500)
    private String observacoes;
    
    @Column(nullable = false)
    private LocalDateTime dataCriacao;
    
    @Column
    private LocalDateTime dataAtualizacao;
    
    @PrePersist
    protected void onCreate() {
        dataCriacao = LocalDateTime.now();
        if (status == null) {
            status = "PENDENTE";
        }
    }
    
    @PreUpdate
    protected void onUpdate() {
        dataAtualizacao = LocalDateTime.now();
    }
}