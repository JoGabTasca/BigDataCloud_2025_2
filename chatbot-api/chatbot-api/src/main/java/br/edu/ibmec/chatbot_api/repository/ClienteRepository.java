package br.edu.ibmec.chatbot_api.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import br.edu.ibmec.chatbot_api.models.Cliente;

@Repository // Indica que essa interface é um repositório do banco de dados
public interface ClienteRepository extends JpaRepository<Cliente, Long> {

}
