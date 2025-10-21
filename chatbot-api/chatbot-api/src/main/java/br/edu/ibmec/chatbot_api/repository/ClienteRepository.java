package br.edu.ibmec.chatbot_api.repository;

import org.springframework.stereotype.Repository;

import com.azure.spring.data.cosmos.repository.CosmosRepository;

import br.edu.ibmec.chatbot_api.models.Cliente;

@Repository // Indica que essa interface é um repositório do banco de dados
public interface ClienteRepository extends CosmosRepository<Cliente, String> {

}
