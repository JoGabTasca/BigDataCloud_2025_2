package br.edu.ibmec.chatbot_api.config;
import org.springframework.boot.context.properties.ConfigurationProperties;

import lombok.Getter;
import lombok.Setter;

@ConfigurationProperties(prefix = "azure.cosmos")
@Getter
@Setter
public class CosmosProperties {
    private String uri;
    private String key;
    private String database;
}
