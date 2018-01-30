FROM java

# Install ElasticSearch.
RUN \
  cd /tmp && \
  wget https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-0.90.13.tar.gz && \
  tar xvzf elasticsearch-0.90.13.tar.gz && \
  rm -f elasticsearch-0.90.13.tar.gz && \
  mv /tmp/elasticsearch-0.90.13 /elasticsearch

# Install Plugins.
RUN \
  /elasticsearch/bin/plugin --install elasticsearch/elasticsearch-mapper-attachments/1.9.0 && \
  /elasticsearch/bin/plugin --install com.github.richardwilly98.elasticsearch/elasticsearch-river-mongodb/1.7.4 && \
  /elasticsearch/bin/plugin --install royrusso/elasticsearch-HQ/1.0.0

# Define mountable directories.
VOLUME ["/data"]

# Define working directory.
WORKDIR /data

# Define default command.
CMD ["/elasticsearch/bin/elasticsearch"]

# Expose ports.
#   - 9200: HTTP
#   - 9300: transport
EXPOSE 9200
EXPOSE 9300