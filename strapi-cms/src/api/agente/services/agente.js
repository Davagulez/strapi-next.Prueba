'use strict';

/**
 * agente service
 */

const { createCoreService } = require('@strapi/strapi').factories;

module.exports = createCoreService('api::agente.agente');
