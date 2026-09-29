import re
from string import Template
import os
import shutil

def select_services():
    print("\n=== Selección de Servicios ===")
    print("Seleccione los servicios a incluir en la cotización:")
    services = {
        'web': input("¿Incluir desarrollo web? (s/n): ").lower() == 's',
        'social': input("¿Incluir redes sociales? (s/n): ").lower() == 's',
        'bot': input("¿Incluir bot de WhatsApp? (s/n): ").lower() == 's',
        'facebook': input("¿Incluir campañas de Facebook? (s/n): ").lower() == 's',
        'ai': input("¿Incluir capacitación en IA? (s/n): ").lower() == 's'
    }
    return services

def parse_price_input(prompt):
    """Prompt until a valid numeric price is entered. Accepts formats like:
       1.234.567, 1234567, 1,234,567.00, 1234567.00, $1.234.567
    """
    while True:
        val = input(prompt).strip()
        # force re-prompt if empty
        if val == "":
            print("Valor requerido. Intente nuevamente.")
            continue
        # remove spaces and currency symbols, keep digits, dots, commas, minus
        cleaned = re.sub(r'[^\d,.-]', '', val)
        # Normalize thousand/decimal separators:
        # - If both ',' and '.' present, assume ',' are thousands separators -> remove commas
        # - If only ',' present, treat ',' as decimal separator -> replace with '.'
        # - Otherwise remove any commas
        if ',' in cleaned and '.' in cleaned:
            cleaned = cleaned.replace(',', '')
        elif ',' in cleaned and '.' not in cleaned:
            cleaned = cleaned.replace(',', '.')
        else:
            cleaned = cleaned.replace(',', '')
        # remove accidental multiple dots
        parts = cleaned.split('.')
        if len(parts) > 2:
            # join all except last as integer part
            cleaned = ''.join(parts[:-1]) + '.' + parts[-1]
        try:
            return float(cleaned)
        except ValueError:
            print("Entrada inválida. Ingrese un número válido (ej: 2000000 o 2.000.000).")

def get_user_input():
    print("=== Sistema de Generación de Cotizaciones ===")
    
    # Client Information
    client_names = input("Ingrese los nombres de los clientes (separados por coma): ")
    client_position = input("Ingrese el cargo del cliente: ")
    
    # Company Information
    company_name = input("Ingrese el nombre de la empresa: ")
    sender_name = input("Ingrese el nombre del remitente: ")
    sender_position = input("Ingrese el cargo del remitente: ")
    
    # Select services
    services = select_services()
    
    # Only ask for prices of selected services, using parser
    prices = {}
    if services['web']:
        prices['web_original'] = parse_price_input("Precio original desarrollo web: ")
        prices['web_discounted'] = parse_price_input("Precio con descuento desarrollo web: ")
    
    if services['social']:
        prices['social_original'] = parse_price_input("Precio original redes sociales: ")
        prices['social_discounted'] = parse_price_input("Precio con descuento redes sociales: ")
    
    if services['bot']:
        prices['bot_original'] = parse_price_input("Precio original bot WhatsApp: ")
        prices['bot_discounted'] = parse_price_input("Precio con descuento bot WhatsApp: ")
    
    if services['facebook']:
        prices['facebook_original'] = parse_price_input("Precio original campañas Facebook: ")
        prices['facebook_discounted'] = parse_price_input("Precio con descuento campañas Facebook: ")
    
    if services['ai']:
        prices['ai_original'] = parse_price_input("Precio original capacitación IA: ")
        prices['ai_discounted'] = parse_price_input("Precio con descuento capacitación IA: ")

    # Offer Terms
    validity_days = input("Días de validez de la oferta: ")
    payment_terms = input("Términos de pago: ")
    
    variables = {
        'client_names': client_names,
        'client_position': client_position,
        'company_name': company_name,
        'sender_name': sender_name,
        'sender_position': sender_position,
        'validity_days': validity_days,
        'payment_terms': payment_terms,
        # Add service text variables
        'web_service': 'Desarrollo web, ' if services['web'] else '',
        'bot_service': 'bot de whatsapp, ' if services['bot'] else '',
        'facebook_service': 'campañas de tráfico pago, ' if services['facebook'] else '',
        'social_service': 'estrategia en redes sociales' if services['social'] else '',
        'ai_service': ' y capacitación en inteligencia artificial' if services['ai'] else '',
        # Add service section content
        'web_section': '''
      <section class="section" id="testimonials">
        <div class="container">
          <div class="row">
            <div class="col-lg-8 offset-lg-2">
              <div class="center-heading">
                <h2>PÁGINA <em>
                  WEB
                </em>
                <p>Características de la página
                </p>
              </h2>

              </div>
            </div>
          </div>
        </div>
      </section>


     
      <section class="section" id="about">
        <div class="container">
            <div class="row">
                <div class="col-lg-4 col-md-6 col-sm-12 col-xs-12"
                    data-scroll-reveal="enter left move 30px over 0.6s after 0.4s">
                    <div class="features-item">
                        <div class="features-icon">
                            <h2>01</h2>
                            <img src="assets/images/features-icon-1.png" alt="">
                            <h4>A medida</h4>
                            <p>Desarrollo completamente a medida, con subpáginas, menús desplegables, botón de WhatsApp y de redes sociales. Tanto los botones, colores, tipografía y en general toda la página.</p>
                        </div>
                    </div>
                </div>
                <div class="col-lg-4 col-md-6 col-sm-12 col-xs-12"
                    data-scroll-reveal="enter bottom move 30px over 0.6s after 0.4s">
                    <div class="features-item">
                        <div class="features-icon">
                            <h2>02</h2>
                            <img src="assets/images/features-icon-2.png" alt="">
                            <h4>Tecnologías</h4>
                            <p>Desarrollo de eccomerce con carrito de compras , diseño responsive que se adapta a diferentes dispositivos (iPad, tablets, computadores, televisores y dispositivos móviles).</p>
                        </div>
                    </div>
                </div>
                <div class="col-lg-4 col-md-6 col-sm-12 col-xs-12"
                    data-scroll-reveal="enter right move 30px over 0.6s after 0.4s">
                    <div class="features-item">
                        <div class="features-icon">
                            <h2>03</h2>
                            <img src="assets/images/features-icon-3.png" alt="">
                            <h4>Posicionamiento SEO</h4>
                            <p>Posicionamiento orgánico, tu página aparece de primera en Google  en los primeros lugares de búsqueda al colocar el nombre de la empresa.</p>
                        </div>
                    </div>
                </div>
                <div class="col-lg-4 col-md-6 col-sm-12 col-xs-12"
                    data-scroll-reveal="enter right move 30px over 0.6s after 0.4s">
                    <div class="features-item">
                        <div class="features-icon">
                            <h2>04</h2>
                            <img src="assets/images/features-icon-3.png" alt="">
                            <h4>UI/UX + mapas de calor</h4>
                            <p>Tú página tendrá una tecnología basada en mapas de calor, donde por medio del diseño minimalista se predice estadísticamente los lugares en que se posicionará el mouse para colocar los botones y llamadas a la acción en dichos lugares.</p>
                        </div>
                    </div>
                </div>
                <div class="col-lg-4 col-md-6 col-sm-12 col-xs-12"
                    data-scroll-reveal="enter right move 30px over 0.6s after 0.4s">
                    <div class="features-item">
                        <div class="features-icon">
                            <h2>05</h2>
                            <img src="assets/images/features-icon-3.png" alt="">
                            <h4>Carrito de compras</h4>
                            <p>Permite agregar productos al carrito de compras y procesar los pagos online ,pagar con difeentes medios de pago.</p>
                        </div>
                    </div>
                </div>
                <div class="col-lg-4 col-md-6 col-sm-12 col-xs-12"
                    data-scroll-reveal="enter right move 30px over 0.6s after 0.4s">
                    <div class="features-item">
                        <div class="features-icon">
                            <h2>06</h2>
                            <img src="assets/images/features-icon-3.png" alt="">
                            <h4>Cuentas de correo</h4>
                            <p>Se incluyen hasta 10 cuentas de correo electrónico (depende del nombre del hosting). Ej: nombre del hosting: nextcompany.com, correo: gerencia@nexthosting.com.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
        ''' if services['web'] else '',
        'social_section': '''       <section class="section" id="testimonials">
        <div class="container">
          <div class="row">
            <div class="col-lg-8 offset-lg-2">
              <div class="center-heading">
                <h2>REDES <em>
                    SOCIALES
                  </em>
                  <p>Características de la estrategia en redes
                  </p>
                </h2>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section class="section" id="about">
        <div class="container">
          <div class="row">
            <div class="col-lg-4 col-md-6 col-sm-12 col-xs-12"
              data-scroll-reveal="enter left move 30px over 0.6s after 0.4s">
              <div class="features-item">
                <div class="features-icon">
                  <h2>01</h2>
                  <img src="assets/images/features-icon-1.png" alt="">
                  <h4>Impulsa tu presencia en redes sociales</h4>
                  <p>Con nuestra inteligencia artificial y nuestro bot especializado, te ofrecemos la oportunidad de
                    impulsar tu presencia en redes sociales.</p>
                </div>
              </div>
            </div>
            <div class="col-lg-4 col-md-6 col-sm-12 col-xs-12"
              data-scroll-reveal="enter bottom move 30px over 0.6s after 0.4s">
              <div class="features-item">
                <div class="features-icon">
                  <h2>02</h2>
                  <img src="assets/images/features-icon-2.png" alt="">
                  <h4>Crecimiento exponencial garantizado</h4>
                  <p>Aprovecha la programación inteligente a través de Facebook Business Suite para conocer las mejores
                    horas de conexión de tus usuarios. Con base en esta información, alcanza tu máximo potencial y obtén
                    un mayor alcance en redes sociales. Además, nuestro uso de hashtags virales te permitirá destacar y
                    captar la atención de una audiencia más amplia. </p>

                </div>
              </div>
            </div>
            <div class="col-lg-4 col-md-6 col-sm-12 col-xs-12"
              data-scroll-reveal="enter right move 30px over 0.6s after 0.4s">
              <div class="features-item">
                <div class="features-icon">
                  <h2>03</h2>
                  <img src="assets/images/features-icon-3.png" alt="">
                  <h4>Optimiza tu estrategia de redes sociales con programación inteligente y hashtags virales.</h4>
                  <p>No solo creamos contenido de valor, sino que también generamos una comunidad alrededor de tu
                    empresa. Nuestra IA y bot te ayudarán a seguir y dejar de seguir cuentas estratégicamente,
                    convirtiendo seguidores en clientes leales. La interacción y la fidelidad que generamos a través de
                    contenido valioso fortalecerán tu marca y te destacarán en tu nicho de mercado.</p>

                </div>
              </div>
            </div>
            <div class="col-lg-4 col-md-6 col-sm-12 col-xs-12"
              data-scroll-reveal="enter right move 30px over 0.6s after 0.4s">
              <div class="features-item">
                <div class="features-icon">
                  <h2>04</h2>
                  <img src="assets/images/features-icon-3.png" alt="">
                  <h4>Crea una comunidad alrededor de tu empresa con contenido valioso.</h4>
                  <p>
                    Nuestro enfoque en el nicho de mercado garantiza que tu estrategia de redes sociales esté dirigida
                    específicamente a tu público objetivo. La automatización inteligente nos permite programar tus posts
                    en las mejores horas de conexión de tus seguidores, maximizando así el impacto y el alcance de tus
                    publicaciones. La combinación de hashtags virales y contenido de valor creará una comunidad
                    comprometida y entusiasta alrededor de tu empresa.
                  </p>

                </div>
              </div>
            </div>
            <div class="col-lg-4 col-md-6 col-sm-12 col-xs-12"
              data-scroll-reveal="enter right move 30px over 0.6s after 0.4s">
              <div class="features-item">
                <div class="features-icon">
                  <h2>05</h2>
                  <img src="assets/images/features-icon-3.png" alt="">
                  <h4>Sácale el máximo provecho a Facebook Business Suite y las mejores horas de conexión.</h4>
                  <p>Optimiza tu presencia en redes sociales con nuestra solución integral. A través de la inteligencia
                    artificial y la programación inteligente, te ofrecemos la posibilidad de aumentar tu visibilidad y
                    alcance en las plataformas más relevantes. Nuestro enfoque en las mejores horas de conexión y el uso
                    estratégico de hashtags virales te ayudarán a alcanzar el mayor potencial en tu estrategia de redes
                    sociales.</p>

                </div>
              </div>
            </div>
            <div class="col-lg-4 col-md-6 col-sm-12 col-xs-12"
              data-scroll-reveal="enter right move 30px over 0.6s after 0.4s">
              <div class="features-item">
                <div class="features-icon">
                  <h2>06</h2>
                  <img src="assets/images/features-icon-3.png" alt="">
                  <h4>Automatización inteligente para el éxito en redes sociales. </h4>
                  <p>Deja que nuestra automatización inteligente se encargue de las tareas diarias en redes sociales,
                    mientras tú te enfocas en tu negocio. Nuestra solución te permitirá delegar el seguimiento y la
                    interacción con cuentas de manera estratégica, generando resultados excepcionales en términos de
                    visibilidad y compromiso. Con nuestro enfoque en la creación de una comunidad sólida, obtendrás
                    clientes leales y un crecimiento sostenible en redes sociales.

                  </p>

                </div>
              </div>
            </div>
          </div>
        </div>
      </section>''' if services['social'] else '',
        'bot_section': '''       <section class="section" id="testimonials">
        <div class="container">
          <div class="row">
            <div class="col-lg-8 offset-lg-2">
              <div class="center-heading">
                <h2>BOT DE <em>
                    WHASTSAPP
                  </em>
                  <p>Características deL BOT
                  </p>
                </h2>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section class="section" id="about">
        <div class="container">
          <div class="row">
            <div class="col-lg-4 col-md-6 col-sm-12 col-xs-12"
              data-scroll-reveal="enter left move 30px over 0.6s after 0.4s">
              <div class="features-item">
                <div class="features-icon">
                  <h2>01</h2>
                  <img src="assets/images/features-icon-1.png" alt="">
                  <h4>Atención ininterrumpida.</h4>
                  <p>El Bot de WhatsApp está disponible las 24 horas del día, los 7 días de la semana.</p>
                </div>
              </div>
            </div>
            <div class="col-lg-4 col-md-6 col-sm-12 col-xs-12"
              data-scroll-reveal="enter bottom move 30px over 0.6s after 0.4s">
              <div class="features-item">
                <div class="features-icon">
                  <h2>02</h2>
                  <img src="assets/images/features-icon-2.png" alt="">
                  <h4>Eficiencia y precisión.</h4>
                  <p>Gracias al uso de Machine Learning, el Bot puede predecir las preguntas y necesidades.</p>
                </div>
              </div>
            </div>
            <div class="col-lg-4 col-md-6 col-sm-12 col-xs-12"
              data-scroll-reveal="enter right move 30px over 0.6s after 0.4s">
              <div class="features-item">
                <div class="features-icon">
                  <h2>03</h2>
                  <img src="assets/images/features-icon-3.png" alt="">
                  <h4>Modelo conversacional avanzado.</h4>
                  <p>El Bot utiliza un modelo conversacional programable y personalizable.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>''' if services['bot'] else '',
        'facebook_section': '''<section class="section" id="testimonials">
        <div class="container">
          <div class="row">
            <div class="col-lg-8 offset-lg-2">
              <div class="center-heading">
                <h2>Campañas de tráfico <em>
                    pago para Facebook
                  </em>
                  <p>Características de las campañas
                  </p>
                </h2>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section class="section" id="about">
        <div class="container">
          <div class="row">
            <div class="col-lg-4 col-md-6 col-sm-12 col-xs-12"
              data-scroll-reveal="enter left move 30px over 0.6s after 0.4s">
              <div class="features-item">
                <div class="features-icon">
                  <h2>01</h2>
                  <img src="assets/images/features-icon-1.png" alt="">
                  <h4>Videos que Conectan y Convierten</h4>
                  <p>Nuestros videos están diseñados con estrategias efectivas que impulsan a los clientes potenciales a contactarte directamente.</p>
                </div>
              </div>
            </div>
            <div class="col-lg-4 col-md-6 col-sm-12 col-xs-12"
              data-scroll-reveal="enter bottom move 30px over 0.6s after 0.4s">
              <div class="features-item">
                <div class="features-icon">
                  <h2>02</h2>
                  <img src="assets/images/features-icon-2.png" alt="">
                  <h4>Inteligencia Artificial al Servicio de tu Marca</h4>
                  <p>Dos videos al mes, optimizados con estrategias SEO y un diseño de copyright atractivo.</p>
                </div>
              </div>
            </div>
            <div class="col-lg-4 col-md-6 col-sm-12 col-xs-12"
              data-scroll-reveal="enter right move 30px over 0.6s after 0.4s">
              <div class="features-item">
                <div class="features-icon">
                  <h2>03</h2>
                  <img src="assets/images/features-icon-3.png" alt="">
                  <h4>Segmentación y Resultados Medibles</h4>
                  <p>Nuestras campañas se segmentan por regiones y se personalizan según las necesidades de tu negocio.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>''' if services['facebook'] else '',
        'ai_section': '''<section class="section" id="testimonials">
        <div class="container">
          <div class="row">
            <div class="col-lg-8 offset-lg-2">
              <div class="center-heading">
                <h2>CAPACITACIÓN EN <em>
                    INTELIGENCIA ARTIFICIAL
                  </em>
                  <p>Características de la capacitación
                  </p>
                </h2>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section class="section" id="about">
        <div class="container">
          <div class="row">
            <div class="col-lg-4 col-md-6 col-sm-12 col-xs-12"
              data-scroll-reveal="enter left move 30px over 0.6s after 0.4s">
              <div class="features-item">
                <div class="features-icon">
                  <h2>01</h2>
                  <img src="assets/images/features-icon-1.png" alt="">
                  <h4>Dominio práctico de herramientas IA</h4>
                  <p>Aprende a usar ChatGPT, GPTs personalizados y plugins de manera efectiva para tu negocio.</p>
                </div>
              </div>
            </div>
            <div class="col-lg-4 col-md-6 col-sm-12 col-xs-12"
              data-scroll-reveal="enter bottom move 30px over 0.6s after 0.4s">
              <div class="features-item">
                <div class="features-icon">
                  <h2>02</h2>
                  <img src="assets/images/features-icon-2.png" alt="">
                  <h4>Presentaciones profesionales</h4>
                  <p>Crea presentaciones impactantes con Gamma.app y otras herramientas de IA complementarias.</p>
                </div>
              </div>
            </div>
            <div class="col-lg-4 col-md-6 col-sm-12 col-xs-12"
              data-scroll-reveal="enter right move 30px over 0.6s after 0.4s">
              <div class="features-item">
                <div class="features-icon">
                  <h2>03</h2>
                  <img src="assets/images/features-icon-3.png" alt="">
                  <h4>Casos prácticos empresariales</h4>
                  <p>Aplicación directa en procesos de ventas, atención al cliente, marketing y generación de documentos.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>''' if services['ai'] else '',
        # Add service flags
        'show_web': 'true' if services['web'] else 'false',
        'show_social': 'true' if services['social'] else 'false',
        'show_bot': 'true' if services['bot'] else 'false',
        'show_facebook': 'true' if services['facebook'] else 'false',
        'show_ai': 'true' if services['ai'] else 'false',
        # Add pricing section content
        'web_pricing': f'''
                <h3>Página web eccomerce</h3><br>
                <s>${format_price(prices.get('web_original', 0))}</s><br>
                ${format_price(prices.get('web_discounted', 0))} ÚNICO PAGO (10% descuento)<br>{payment_terms}<br>
                <br>
        ''' if services['web'] else '',
        
        'social_pricing': f'''
                <h3>Redes Sociales</h3><br>
                <s>${format_price(prices.get('social_original', 0))}</s><br>
                ${format_price(prices.get('social_discounted', 0))} VALOR MENSUAL (10% descuento)<br>{payment_terms}<br>
                <br>
        ''' if services['social'] else '',
        
        'bot_pricing': f'''
                <h3>Bot de whatsapp</h3><br>
                <s>${format_price(prices.get('bot_original', 0))}</s><br>
                ${format_price(prices.get('bot_discounted', 0))} VALOR ANUAL (10% descuento)<br>{payment_terms}<br>
                <br>
        ''' if services['bot'] else '',
        
        'facebook_pricing': f'''
                <h3>Campañas de tráfico pago para Facebook</h3><br>
                <s>${format_price(prices.get('facebook_original', 0))}</s><br>
                ${format_price(prices.get('facebook_discounted', 0))} VALOR MENSUAL (10% descuento)<br>{payment_terms}<br>
                <br>
        ''' if services['facebook'] else '',
        
        'ai_pricing': f'''
                <h3>Capacitación en herramientas de inteligencia artificial</h3><br>
                <s>${format_price(prices.get('ai_original', 0))}</s><br>
                ${format_price(prices.get('ai_discounted', 0))} ÚNICO PAGO (10% descuento)<br>{payment_terms}<br>
                <br>
                <br>
        ''' if services['ai'] else '',
    }

    # initialize all price variables (so template has keys)
    price_keys = ['web_original','web_discounted','social_original','social_discounted',
                  'bot_original','bot_discounted','facebook_original','facebook_discounted',
                  'ai_original','ai_discounted']
    for k in price_keys:
        variables[k] = format_price(0)
    # Add prices only for selected services (overwrite defaults)
    for service, price_data in prices.items():
        variables[service] = format_price(price_data)

    return variables

def format_price(price):
    return "{:,.0f}".format(price).replace(",", ".")

def get_variables_from_data(data):
    """Convert GUI data format to backend variables format"""
    services = data['services']
    prices = data['prices']
    
    variables = {
        'client_names': data['client_names'],
        'client_position': data['client_position'],
        'company_name': data['company_name'],
        'sender_name': data['sender_name'],
        'sender_position': data['sender_position'],
        'validity_days': data['validity_days'],
        'payment_terms': data['payment_terms'],
        
        # Add service text variables
        'web_service': 'Desarrollo web, ' if services['web'] else '',
        'bot_service': 'bot de whatsapp, ' if services['bot'] else '',
        'facebook_service': 'campañas de tráfico pago, ' if services['facebook'] else '',
        'social_service': 'estrategia en redes sociales' if services['social'] else '',
        'ai_service': ' y capacitación en inteligencia artificial' if services['ai'] else '',
        
        # Add service flags
        'show_web': 'true' if services['web'] else 'false',
        'show_social': 'true' if services['social'] else 'false',
        'show_bot': 'true' if services['bot'] else 'false',
        'show_facebook': 'true' if services['facebook'] else 'false',
        'show_ai': 'true' if services['ai'] else 'false',
        
        # Add service section content (using the same logic as get_user_input)
        'web_section': '''
      <section class="section" id="testimonials">
        <div class="container">
          <div class="row">
            <div class="col-lg-8 offset-lg-2">
              <div class="center-heading">
                <h2>PÁGINA <em>
                  WEB
                </em>
                <p>Características de la página
                </p>
              </h2>
              </div>
            </div>
          </div>
        </div>
      </section>
      <section class="section" id="about">
        <div class="container">
            <div class="row">
                <div class="col-lg-4 col-md-6 col-sm-12 col-xs-12"
                    data-scroll-reveal="enter left move 30px over 0.6s after 0.4s">
                    <div class="features-item">
                        <div class="features-icon">
                            <h2>01</h2>
                            <img src="assets/images/features-icon-1.png" alt="">
                            <h4>A medida</h4>
                            <p>Desarrollo completamente a medida, con subpáginas, menús desplegables, botón de WhatsApp y de redes sociales. Tanto los botones, colores, tipografía y en general toda la página.</p>
                        </div>
                    </div>
                </div>
                <div class="col-lg-4 col-md-6 col-sm-12 col-xs-12"
                    data-scroll-reveal="enter bottom move 30px over 0.6s after 0.4s">
                    <div class="features-item">
                        <div class="features-icon">
                            <h2>02</h2>
                            <img src="assets/images/features-icon-2.png" alt="">
                            <h4>Tecnologías</h4>
                            <p>Desarrollo de eccomerce con carrito de compras , diseño responsive que se adapta a diferentes dispositivos (iPad, tablets, computadores, televisores y dispositivos móviles).</p>
                        </div>
                    </div>
                </div>
                <div class="col-lg-4 col-md-6 col-sm-12 col-xs-12"
                    data-scroll-reveal="enter right move 30px over 0.6s after 0.4s">
                    <div class="features-item">
                        <div class="features-icon">
                            <h2>03</h2>
                            <img src="assets/images/features-icon-3.png" alt="">
                            <h4>Posicionamiento SEO</h4>
                            <p>Posicionamiento orgánico, tu página aparece de primera en Google  en los primeros lugares de búsqueda al colocar el nombre de la empresa.</p>
                        </div>
                    </div>
                </div>
                <div class="col-lg-4 col-md-6 col-sm-12 col-xs-12"
                    data-scroll-reveal="enter right move 30px over 0.6s after 0.4s">
                    <div class="features-item">
                        <div class="features-icon">
                            <h2>04</h2>
                            <img src="assets/images/features-icon-3.png" alt="">
                            <h4>UI/UX + mapas de calor</h4>
                            <p>Tú página tendrá una tecnología basada en mapas de calor, donde por medio del diseño minimalista se predice estadísticamente los lugares en que se posicionará el mouse para colocar los botones y llamadas a la acción en dichos lugares.</p>
                        </div>
                    </div>
                </div>
                <div class="col-lg-4 col-md-6 col-sm-12 col-xs-12"
                    data-scroll-reveal="enter right move 30px over 0.6s after 0.4s">
                    <div class="features-item">
                        <div class="features-icon">
                            <h2>05</h2>
                            <img src="assets/images/features-icon-3.png" alt="">
                            <h4>Carrito de compras</h4>
                            <p>Permite agregar productos al carrito de compras y procesar los pagos online ,pagar con difeentes medios de pago.</p>
                        </div>
                    </div>
                </div>
                <div class="col-lg-4 col-md-6 col-sm-12 col-xs-12"
                    data-scroll-reveal="enter right move 30px over 0.6s after 0.4s">
                    <div class="features-item">
                        <div class="features-icon">
                            <h2>06</h2>
                            <img src="assets/images/features-icon-3.png" alt="">
                            <h4>Cuentas de correo</h4>
                            <p>Se incluyen hasta 10 cuentas de correo electrónico (depende del nombre del hosting). Ej: nombre del hosting: nextcompany.com, correo: gerencia@nexthosting.com.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
        ''' if services['web'] else '',
        'social_section': '''       <section class="section" id="testimonials">
        <div class="container">
          <div class="row">
            <div class="col-lg-8 offset-lg-2">
              <div class="center-heading">
                <h2>REDES <em>
                    SOCIALES
                  </em>
                  <p>Características de las redes
                  </p>
                </h2>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section class="section" id="about">
        <div class="container">
          <div class="row">
            <div class="col-lg-4 col-md-6 col-sm-12 col-xs-12"
              data-scroll-reveal="enter left move 30px over 0.6s after 0.4s">
              <div class="features-item">
                <div class="features-icon">
                  <h2>01</h2>
                  <img src="assets/images/features-icon-1.png" alt="">
                  <h4>Estrategia basada en investigación de mercado</h4>
                  <p>Con la investigación de mercado realizada, obtendrás una estrategia de contenido personalizada
                    para tu audiencia específica.</p>

                </div>
              </div>
            </div>
            <div class="col-lg-4 col-md-6 col-sm-12 col-xs-12"
              data-scroll-reveal="enter bottom move 30px over 0.6s after 0.6s after 0.4s">
              <div class="features-item">
                <div class="features-icon">
                  <h2>02</h2>
                  <img src="assets/images/features-icon-2.png" alt="">
                  <h4>Crecimiento exponencial garantizado</h4>
                  <p>Aprovecha la programación inteligente a través de Facebook Business Suite para conocer las mejores
                    horas de conexión de tus usuarios.</p>

                </div>
              </div>
            </div>
            <div class="col-lg-4 col-md-6 col-sm-12 col-xs-12"
              data-scroll-reveal="enter right move 30px over 0.6s after 0.4s">
              <div class="features-item">
                <div class="features-icon">
                  <h2>03</h2>
                  <img src="assets/images/features-icon-3.png" alt="">
                  <h4>Hashtags virales y alcance masivo</h4>
                  <p>Nuestro análisis de tendencias y uso estratégico de hashtags virales te ayudarán a alcanzar el mayor potencial en tu estrategia de redes sociales.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>''' if services['social'] else '',
        'bot_section': '''       <section class="section" id="testimonials">
        <div class="container">
          <div class="row">
            <div class="col-lg-8 offset-lg-2">
              <div class="center-heading">
                <h2>BOT DE <em>
                    WHASTSAPP
                  </em>
                  <p>Características deL BOT
                  </p>
                </h2>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section class="section" id="about">
        <div class="container">
          <div class="row">
            <div class="col-lg-4 col-md-6 col-sm-12 col-xs-12"
              data-scroll-reveal="enter left move 30px over 0.6s after 0.4s">
              <div class="features-item">
                <div class="features-icon">
                  <h2>01</h2>
                  <img src="assets/images/features-icon-1.png" alt="">
                  <h4>Atención ininterrumpida.</h4>
                  <p>El Bot de WhatsApp está disponible las 24 horas del día, los 7 días de la semana.</p>
                </div>
              </div>
            </div>
            <div class="col-lg-4 col-md-6 col-sm-12 col-xs-12"
              data-scroll-reveal="enter bottom move 30px over 0.6s after 0.4s">
              <div class="features-item">
                <div class="features-icon">
                  <h2>02</h2>
                  <img src="assets/images/features-icon-2.png" alt="">
                  <h4>Eficiencia y precisión.</h4>
                  <p>Gracias al uso de Machine Learning, el Bot puede predecir las preguntas y necesidades.</p>
                </div>
              </div>
            </div>
            <div class="col-lg-4 col-md-6 col-sm-12 col-xs-12"
              data-scroll-reveal="enter right move 30px over 0.6s after 0.4s">
              <div class="features-item">
                <div class="features-icon">
                  <h2>03</h2>
                  <img src="assets/images/features-icon-3.png" alt="">
                  <h4>Modelo conversacional avanzado.</h4>
                  <p>El Bot utiliza un modelo conversacional programable y personalizable.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>''' if services['bot'] else '',
        'facebook_section': '''<section class="section" id="testimonials">
        <div class="container">
          <div class="row">
            <div class="col-lg-8 offset-lg-2">
              <div class="center-heading">
                <h2>Campañas de tráfico <em>
                    pago para Facebook
                  </em>
                  <p>Características de las campañas
                  </p>
                </h2>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section class="section" id="about">
        <div class="container">
          <div class="row">
            <div class="col-lg-4 col-md-6 col-sm-12 col-xs-12"
              data-scroll-reveal="enter left move 30px over 0.6s after 0.4s">
              <div class="features-item">
                <div class="features-icon">
                  <h2>01</h2>
                  <img src="assets/images/features-icon-1.png" alt="">
                  <h4>Videos que Conectan y Convierten</h4>
                  <p>Nuestros videos están diseñados con estrategias efectivas que impulsan a los clientes potenciales a contactarte directamente.</p>
                </div>
              </div>
            </div>
            <div class="col-lg-4 col-md-6 col-sm-12 col-xs-12"
              data-scroll-reveal="enter bottom move 30px over 0.6s after 0.4s">
              <div class="features-item">
                <div class="features-icon">
                  <h2>02</h2>
                  <img src="assets/images/features-icon-2.png" alt="">
                  <h4>Inteligencia Artificial al Servicio de tu Marca</h4>
                  <p>Dos videos al mes, optimizados con estrategias SEO y un diseño de copyright atractivo.</p>
                </div>
              </div>
            </div>
            <div class="col-lg-4 col-md-6 col-sm-12 col-xs-12"
              data-scroll-reveal="enter right move 30px over 0.6s after 0.4s">
              <div class="features-item">
                <div class="features-icon">
                  <h2>03</h2>
                  <img src="assets/images/features-icon-3.png" alt="">
                  <h4>Segmentación y Resultados Medibles</h4>
                  <p>Nuestras campañas se segmentan por regiones y se personalizan según las necesidades de tu negocio.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>''' if services['facebook'] else '',
        'ai_section': '''<section class="section" id="testimonials">
        <div class="container">
          <div class="row">
            <div class="col-lg-8 offset-lg-2">
              <div class="center-heading">
                <h2>CAPACITACIÓN EN <em>
                    INTELIGENCIA ARTIFICIAL
                  </em>
                  <p>Características de la capacitación
                  </p>
                </h2>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section class="section" id="about">
        <div class="container">
          <div class="row">
            <div class="col-lg-4 col-md-6 col-sm-12 col-xs-12"
              data-scroll-reveal="enter left move 30px over 0.6s after 0.4s">
              <div class="features-item">
                <div class="features-icon">
                  <h2>01</h2>
                  <img src="assets/images/features-icon-1.png" alt="">
                  <h4>Formación Práctica y Aplicada</h4>
                  <p>Curso completamente enfocado en la práctica, donde cada participante aprenderá haciendo, con casos reales aplicados a su trabajo.</p>
                </div>
              </div>
            </div>
            <div class="col-lg-4 col-md-6 col-sm-12 col-xs-12"
              data-scroll-reveal="enter bottom move 30px over 0.6s after 0.4s">
              <div class="features-item">
                <div class="features-icon">
                  <h2>02</h2>
                  <img src="assets/images/features-icon-2.png" alt="">
                  <h4>Herramientas Avanzadas de IA</h4>
                  <p>Dominio de ChatGPT, GPTs personalizados, Gamma.app para presentaciones y plugins especializados que aumentan la productividad.</p>
                </div>
              </div>
            </div>
            <div class="col-lg-4 col-md-6 col-sm-12 col-xs-12"
              data-scroll-reveal="enter right move 30px over 0.6s after 0.4s">
              <div class="features-item">
                <div class="features-icon">
                  <h2>03</h2>
                  <img src="assets/images/features-icon-3.png" alt="">
                  <h4>Soporte Continuo y Material Completo</h4>
                  <p>Material de apoyo descargable, grabaciones de todas las sesiones y resolución de dudas en tiempo real durante la capacitación.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>''' if services['ai'] else '',
        
        # Add pricing section content
        'web_pricing': f'''
                <h3>Página web eccomerce</h3><br>
                <s>${format_price(prices.get('web_original', 0))}</s><br>
                ${format_price(prices.get('web_discounted', 0))} ÚNICO PAGO (10% descuento)<br>{data['payment_terms']}<br>
                <br>
        ''' if services['web'] else '',
        
        'social_pricing': f'''
                <h3>Redes Sociales</h3><br>
                <s>${format_price(prices.get('social_original', 0))}</s><br>
                ${format_price(prices.get('social_discounted', 0))} VALOR MENSUAL (10% descuento)<br>{data['payment_terms']}<br>
                <br>
        ''' if services['social'] else '',
        
        'bot_pricing': f'''
                <h3>Bot de whatsapp</h3><br>
                <s>${format_price(prices.get('bot_original', 0))}</s><br>
                ${format_price(prices.get('bot_discounted', 0))} VALOR ANUAL (10% descuento)<br>{data['payment_terms']}<br>
                <br>
        ''' if services['bot'] else '',
        
        'facebook_pricing': f'''
                <h3>Campañas de tráfico pago para Facebook</h3><br>
                <s>${format_price(prices.get('facebook_original', 0))}</s><br>
                ${format_price(prices.get('facebook_discounted', 0))} VALOR MENSUAL (10% descuento)<br>{data['payment_terms']}<br>
                <br>
        ''' if services['facebook'] else '',
        
        'ai_pricing': f'''
                <h3>Capacitación en herramientas de inteligencia artificial</h3><br>
                <s>${format_price(prices.get('ai_original', 0))}</s><br>
                ${format_price(prices.get('ai_discounted', 0))} ÚNICO PAGO (10% descuento)<br>{data['payment_terms']}<br>
                <br>
                ✅ Dominio práctico de ChatGPT, GPTs personalizados y uso efectivo de plugins<br>
                ✅ Creación de presentaciones profesionales con Gamma.app y herramientas IA complementarias<br>
                ✅ Casos prácticos orientados a los procesos de la empresa<br>
                ✅ Material de apoyo y grabaciones<br>
                ✅ Resolución de dudas en tiempo real<br>
                ✅ Recomendaciones específicas para maximizar el retorno de inversión en IA<br>
        ''' if services['ai'] else '',
    }

    # Initialize all price variables (so template has keys)
    price_keys = ['web_original','web_discounted','social_original','social_discounted',
                  'bot_original','bot_discounted','facebook_original','facebook_discounted',
                  'ai_original','ai_discounted']
    for k in price_keys:
        variables[k] = format_price(0)
    
    # Add prices only for selected services (overwrite defaults)
    for service, price_data in prices.items():
        variables[service] = format_price(price_data)

    return variables

def remove_duplicate_footer(html: str) -> str:
    """Keep first <footer id="contact-us">...</footer>, remove subsequent ones,
    then trim content after the first </html> (if extras were appended)."""
    # find all contact-us footer matches
    pattern = re.compile(r'(<footer\b[^>]*\bid=["\']contact-us["\'][\s\S]*?</footer>)', re.IGNORECASE)
    matches = list(pattern.finditer(html))
    
    if len(matches) <= 1:
        # ensure single closing html
        first_html = html.find("</html>")
        return html if first_html == -1 else html[:first_html + len("</html>")]
    # remove all subsequent matches (from the end to keep indexes valid)
    cleaned = html
    for m in reversed(matches[1:]):
        cleaned = cleaned[:m.start()] + cleaned[m.end():]
    # trim anything after the first </html> to remove duplicated scripts/closing tags
    first_html = cleaned.find("</html>")
    if first_html != -1:
        cleaned = cleaned[:first_html + len("</html>")]
    return cleaned

def sanitize_folder_name(name):
    """Convert client name to a valid folder name"""
    # Remove or replace invalid characters for folder names
    sanitized = re.sub(r'[<>:"/\\|?*]', '', name)
    sanitized = re.sub(r'\s+', '_', sanitized.strip())
    return sanitized[:50]  # Limit length to avoid issues

def generate_client_folder_structure(template_path, client_name, variables):
    """Generate the complete client folder structure with assets"""
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Create sanitized client folder name
        folder_name = sanitize_folder_name(client_name)
        if not folder_name:
            folder_name = "Cliente_Sin_Nombre"
        
        # Create paths with cotizaciones folder
        cotizaciones_folder = os.path.join(current_dir, "cotizaciones")
        client_folder = os.path.join(cotizaciones_folder, folder_name)
        to_upload_folder = os.path.join(client_folder, "to_upload")
        assets_destination = os.path.join(to_upload_folder, "assets")
        assets_source = os.path.join(current_dir, "assets")
        
        # Create directories
        os.makedirs(to_upload_folder, exist_ok=True)
        
        # Copy assets folder
        if os.path.exists(assets_source):
            if os.path.exists(assets_destination):
                shutil.rmtree(assets_destination)
            shutil.copytree(assets_source, assets_destination)
        
        # Generate HTML
        with open(template_path, 'r', encoding='utf-8') as file:
            template_content = file.read()
        
        template = Template(template_content)
        filled_template = template.safe_substitute(variables)
        
        # Remove duplicated footer blocks if present
        cleaned_html = remove_duplicate_footer(filled_template)
        
        # Save as index.html in to_upload folder
        index_path = os.path.join(to_upload_folder, "index.html")
        with open(index_path, 'w', encoding='utf-8') as file:
            file.write(cleaned_html)
        
        return client_folder, index_path
        
    except Exception as e:
        print(f"Error creating client folder structure: {str(e)}")
        return None, None

def generate_html(template_path, output_path, variables):
    """Legacy function for backward compatibility"""
    try:
        with open(template_path, 'r', encoding='utf-8') as file:
            template_content = file.read()
        
        template = Template(template_content)
        filled_template = template.safe_substitute(variables)

        # Remove duplicated footer blocks if present
        cleaned_html = remove_duplicate_footer(filled_template)
        
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(cleaned_html)
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def main():
    # Define paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(current_dir, 'template.html')
    
    # Get user input
    variables = get_user_input()
    
    # Generate client folder structure
    client_name = variables.get('company_name', variables.get('client_names', 'Cliente'))
    client_folder, index_path = generate_client_folder_structure(template_path, client_name, variables)
    
    if client_folder and index_path:
        print(f"\n✅ Cotización generada exitosamente!")
        print(f"📁 Carpeta del cliente: {client_folder}")
        print(f"🌐 Archivo principal: {index_path}")
        print(f"📋 Listo para subir: {os.path.join(client_folder, 'to_upload')}")
    else:
        print("❌ Error al generar la cotización")

if __name__ == "__main__":
    main()
