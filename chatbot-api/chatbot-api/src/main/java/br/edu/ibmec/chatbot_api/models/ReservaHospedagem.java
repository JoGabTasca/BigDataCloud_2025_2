package br.edu.ibmec.chatbot_api.models;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Entity
@Table(name = "reserva_hospedagem")
public class ReservaHospedagem {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false)
    private Long clienteId;
    
    @Column(nullable = false, length = 150)
    private String nomeHotel;
    
    @Column(nullable = false, length = 100)
    private String cidade;
    
    @Column(nullable = false, length = 200)
    private String endereco;
    
    @Column(nullable = false)
    private LocalDate dataCheckIn;
    
    @Column(nullable = false)
    private LocalDate dataCheckOut;
    
    @Column(nullable = false, length = 100)
    private String tipoQuarto; // STANDARD, DELUXE, SUITE, PRESIDENCIAL
    
    @Column(length = 20)
    private String numeroQuarto;
    
    @Column(nullable = false)
    private Integer numeroHospedes;
    
    @Column(nullable = false, precision = 10, scale = 2)
    private BigDecimal precoPorNoite;
    
    @Column(nullable = false, precision = 10, scale = 2)
    private BigDecimal precoTotal;
    
    @Column(nullable = false, length = 50)
    private String status; // CONFIRMADA, CANCELADA, PENDENTE
    
    @Column(length = 500)
    private String observacoes;
    
    @Column(length = 20)
    private String telefoneHotel;
    
    @Column(length = 100)
    private String emailHotel;
    
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