FROM vijaybalebail/python
RUN pip3.6 install bottle && \
    python3.6 -m pip install bottle && \
    pip3.6 install flask && \
    python3.6 -m pip install flask &&\
    pip3.6 install requests &&\
    python3.6 -m pip install requests 


ENV PYTHONUNBUFFERED=1
WORKDIR /myapp
ADD  requirements.txt /myapp
RUN pip install -r requirements.txt

EXPOSE 8080
ADD main.py /myapp
ADD config.json /myapp
ADD IdcsClient.py /myapp
ADD Constants.py /myapp
ADD templates /myapp/templates
ADD imgs      /myapp/templates/imgs

#CMD exec python3.6 query.py
#CMD exec python3.6 a.py
CMD exec python3.6 main.py
