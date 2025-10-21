package br.edu.ibmec.chatbot_api.models;

import lombok.Data;

import java.time.LocalDateTime;

@Data
public class ReservaVoo {

    private Long id;

    private String origem;

    private String destino;

    private LocalDateTime dataHoraPartida;

    private LocalDateTime dataHoraVolta;

    private String classe; // ECONOMICA, EXECUTIVA, PRIMEIRA_CLASSE

    private String status; // CONFIRMADA, CANCELADA, PENDENTE

    private String observacoes;

    private LocalDateTime dataCriacao;

    private LocalDateTime dataAtualizacao;
}