$(document).ready(function(){

  // Dades identificatives - Càrrecs directius - Històric

  if( $('.historic').length == 0 ){
    $('.notHistoric').show();
    $('.hasHistoric').hide();
  }

  $('.historic').hide();
  $('#historicDadesIdentificatives').on('click', function(){
    this.checked ? $('.historic').show(300) : $('.historic').hide(300);
  });

  // Dades identificatives - Observacions

  $('.observacions').hide();
  $('#observacionsDadesIdentificatives').on('click', function(){
    this.checked ? $('.observacions').show(300) : $('.observacions').hide(300);
  });

  // Participació de la UPC - 1. Al capital social o fons patrimonial - Observacions

  $('.observacionsCapital').hide();
  $('#observacionsCapitalDadesIdentificatives').on('click', function(){
    this.checked ? $('.observacionsCapital').show(300) : $('.observacionsCapital').hide(300);
  });

  // Participació de la UPC - 2. A òrgan de govern superior - Observacions

  $('.observacionsMembres').hide();
  $('#observacionsMembresDadesIdentificatives').on('click', function(){
    this.checked ? $('.observacionsMembres').show(300) : $('.observacionsMembres').hide(300);
  });

  // Participació de la UPC - 3. Quota anual - Observacions

  $('.observacionsQuota').hide();
  $('#observacionsQuotaDadesIdentificatives').on('click', function(){
    this.checked ? $('.observacionsQuota').show(300) : $('.observacionsQuota').hide(300);
  });

  // Participació de la UPC - Òrgans de govern

  $('.composicioOGParticipacio').hide();
  $('.composicioOGParticipacioSwitch').on('click', function(){
    this.checked ?
      $(this).parent().children('.composicioOGParticipacio').show(300) :
      $(this).parent().children('.composicioOGParticipacio').hide(300);
  });

  $('.sectionOGParticipacio').each(function(){

    if( $(this).find('.historicCarrecOGParticipacio').length == 0 ){
      $(this).find('.notHistoricCarrecOGParticipacio').show();
      $(this).find('.hasHistoricCarrecOGParticipacio').hide();
    }

  });

  $('.historicCarrecOGParticipacio').hide();
  $('.historicCarrecOGParticipacioSwitch').on('click', function(){
    debugger;
    this.checked ?
      $(this).parent().parent().find('.historicCarrecOGParticipacio').show(300) :
      $(this).parent().parent().find('.historicCarrecOGParticipacio').hide(300);
  });

  // Participació de la UPC - Òrgans assessors

  $('.composicioOGAssessorsParticipacio').hide();
  $('.composicioOGAssessorsParticipacioSwitch').on('click', function(){
    this.checked ?
      $(this).parent().children('.composicioOGAssessorsParticipacio').show(300) :
      $(this).parent().children('.composicioOGAssessorsParticipacio').hide(300);
  });

  $('.sectionOGAssessorsParticipacio').each(function(){

    if( $(this).find('.historicCarrecOGAssessorsParticipacio').length == 0 ){
      $(this).find('.notHistoricCarrecOGAssessorsParticipacio').show();
      $(this).find('.hasHistoricCarrecOGAssessorsParticipacio').hide();
    }

  });

  $('.historicCarrecOGAssessorsParticipacio').hide();
  $('.historicCarrecOGAssessorsParticipacioSwitch').on('click', function(){
    debugger;
    this.checked ?
      $(this).parent().parent().find('.historicCarrecOGAssessorsParticipacio').show(300) :
      $(this).parent().parent().find('.historicCarrecOGAssessorsParticipacio').hide(300);
  });

  // Marc Legal - Observacions

  $('.observacionsLegal').hide();
  $('#observacionsMarcLegal').on('click', function(){
    this.checked ? $('.observacionsLegal').show(300) : $('.observacionsLegal').hide(300);
  });

});