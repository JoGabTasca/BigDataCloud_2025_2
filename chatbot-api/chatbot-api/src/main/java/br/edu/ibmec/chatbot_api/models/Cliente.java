package br.edu.ibmec.chatbot_api.models;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import lombok.Data;

@Data // Gera getters, setters, toString, equals e hashCode automaticamente
@Entity // Indica que essa classe é uma entidade do banco de dados
public class Cliente {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column
    private String nome;
    @Column
    private String email;
    @Column
    private String cpf;
    @Column
    private String telefone;
}
