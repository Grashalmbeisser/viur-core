# -*- coding: utf-8 -*-
from server.applications.list import List
from server.skeleton import SkelList
from server.bones import *
from server import errors, session, conf, request, exposed, internalExposed
from server import utils
import json

class Cart( List ):
	listTemplate = "order_viewcart"
	adminInfo = None
	productSkel = None

	@exposed
	def add( self, product, amt=None, extend=False, async=False ):
		"""
		Adds the product with the id product to the cart.
		If product already exists, and amt is left-out, the number of the product in the cart will be increased.

		:param product: The product key to add to the cart.
		:param amt: The amount to add; default is 1.
		:param extend: Set True, if amt should be added to existing items, else the amount is overridden.
		:param async: Set True for use in Ajax requests.
		"""

		prods = session.current.get("cart_products") or {}
		if not isinstance(extend, bool):
			extend = bool(int(extend))
		if not isinstance(async, bool):
			async = bool(int(async))

		if not all( x in "1234567890" for x in unicode(amt) ):
			amt = None

		if self.productSkel().fromDB( product ):
			if not product in prods.keys():
				prods[ product ] = { "amount" : 0 }

			if amt and not bool( extend ):
				prods[ product ][ "amount" ] = int(amt)
			else:
				if amt is None:
					amt = 1

				prods[ product ][ "amount" ] += int( amt )

			session.current["cart_products"] = prods
			session.current.markChanged()

		if async:
			return json.dumps({ "cartentries": self.entryCount(),
			                    "cartsum": self.cartSum(),
			                    "added": int( amt ) } )

		raise( errors.Redirect( "/%s/view" % self.modulName ) )

	@exposed
	def view( self, *args, **kwargs ):
		prods = session.current.get("cart_products") or {}

		if prods:
			items = self.productSkel().all().mergeExternalFilter( {"id": list(prods.keys()) } ).fetch( limit=10 )
		else:
			items = SkelList( self.productSkel )

		for skel in items:
			skel["amt"] = numericBone( descr="Quantity",
			                defaultValue = session.current["cart_products"][ str( skel["id"].value ) ][ "amount" ] )

		return( self.render.list( items ) )

	@exposed
	def delete( self, product, all="0", async=False ):
		"""
		Deletes or decrements a product from the cart.
		If all is set, it removes the entire product.

		:param product: The product key to add to the cart.
		:param all: If not "0", remove the entire entry for product, else decrement.
		:param async: Set True for use in Ajax requests.
		"""

		prods = session.current.get("cart_products") or {}

		if product in prods.keys():
			removed = prods[ product ][ "amount" ]

			if all=="0" and prods[ product ][ "amount" ] > 1:
				prods[ product ][ "amount" ] -= 1
			else:
				del prods[ product ]
		else:
			removed = 0

		session.current["cart_products"] = prods
		session.current.markChanged()

		if async:
			return json.dumps({ "cartentries": self.entryCount(),
			                    "cartsum": self.cartSum(),
			                    "removed": removed })

		raise( errors.Redirect( "/%s/view" % self.modulName ) )

	@internalExposed
	def entryCount( self ):
		prods = session.current.get("cart_products") or {}
		return( len( prods.keys() ) )

	@internalExposed
	def cartSum( self ):
		# Should be overridden.
		return 0.0
