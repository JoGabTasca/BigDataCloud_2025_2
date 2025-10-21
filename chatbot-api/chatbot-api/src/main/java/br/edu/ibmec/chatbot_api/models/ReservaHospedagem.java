package br.edu.ibmec.chatbot_api.models;

import lombok.Data;

import java.time.LocalDate;
import java.time.LocalDateTime;

@Data
public class ReservaHospedagem {

    private Long id;

    private String nomeHotel;

    private String cidade;

    private String endereco;

    private LocalDate dataCheckIn;

    private LocalDate dataCheckOut;

    private String tipoQuarto; // STANDARD, DELUXE, SUITE, PRESIDENCIAL

    private Integer numeroHospedes;

    private String status; // CONFIRMADA, CANCELADA, PENDENTE

    private String observacoes;

    private LocalDateTime dataCriacao;

    private LocalDateTime dataAtualizacao;
}