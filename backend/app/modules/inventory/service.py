from uuid import uuid4

from sqlalchemy.orm import Session

from app.modules.inventory.constants import InventoryMovementType
from app.modules.inventory.movement_service import (
    InventoryMovementService,
)
from app.modules.inventory.model import Inventory
from app.modules.inventory.repository import InventoryRepository
from app.modules.inventory.schema import (
    InventoryCreate,
    InventoryFilter,
    InventoryUpdate,
    StockAdjustment,
    StockTransfer,
)
from app.modules.organizations.repository import OrganizationRepository
from app.modules.products.repository import ProductRepository
from app.modules.warehouses.repository import WarehouseRepository


class InventoryService:

    # ==========================================
    # Create Inventory
    # ==========================================

    @staticmethod
    def create(
        db: Session,
        inventory_data: InventoryCreate,
        organization_id: str,
        user_id: str,
    ) -> Inventory:

        # Validate organization
        organization = OrganizationRepository.get_by_id(
            db,
            organization_id,
        )

        if organization is None:
            raise ValueError(
                "Organization not found."
            )

        # Validate warehouse
        warehouse = WarehouseRepository.get_by_id(
            db,
            inventory_data.warehouse_id,
        )

        if warehouse is None:
            raise ValueError(
                "Warehouse not found."
            )

        if warehouse.organization_id != organization_id:
            raise ValueError(
                "Warehouse does not belong to this organization."
            )

        if not warehouse.is_active:
            raise ValueError(
                "Warehouse is inactive."
            )

        # Validate product
        product = ProductRepository.get_by_id(
            db,
            inventory_data.product_id,
        )

        if product is None:
            raise ValueError(
                "Product not found."
            )

        if product.organization_id != organization_id:
            raise ValueError(
                "Product does not belong to this organization."
            )

        # Prevent duplicate inventory record
        existing = InventoryRepository.get_by_product_and_warehouse(
            db,
            organization_id,
            inventory_data.product_id,
            inventory_data.warehouse_id,
        )

        if existing:
            raise ValueError(
                "Inventory already exists for this product and warehouse."
            )

        # Reserved quantity cannot exceed quantity
        if (
            inventory_data.reserved_quantity
            > inventory_data.quantity
        ):
            raise ValueError(
                "Reserved quantity cannot exceed available stock."
            )

        # Max stock validation
        if (
            inventory_data.max_stock_level > 0
            and inventory_data.quantity
            > inventory_data.max_stock_level
        ):
            raise ValueError(
                "Quantity cannot exceed maximum stock level."
            )

        inventory = Inventory(
            id=str(uuid4()),
            organization_id=organization_id,

            warehouse_id=inventory_data.warehouse_id,
            product_id=inventory_data.product_id,

            quantity=inventory_data.quantity,
            reserved_quantity=inventory_data.reserved_quantity,

            reorder_level=inventory_data.reorder_level,
            max_stock_level=inventory_data.max_stock_level,

            created_by=user_id,
            updated_by=user_id,
        )

        return InventoryRepository.create(
            db,
            inventory,
        )

    # ==========================================
    # Get By ID
    # ==========================================

    @staticmethod
    def get_by_id(
        db: Session,
        inventory_id: str,
        organization_id: str,
    ):

        inventory = InventoryRepository.get_by_id(
            db,
            inventory_id,
        )

        if inventory is None:
            return None

        if inventory.organization_id != organization_id:
            return None

        return inventory

    # ==========================================
    # Get All
    # ==========================================

    @staticmethod
    def get_all(
        db: Session,
        organization_id: str,
        skip: int = 0,
        limit: int = 20,
    ):

        return {
            "total": InventoryRepository.count(
                db,
                organization_id,
            ),
            "items": InventoryRepository.get_all(
                db,
                organization_id,
                skip=skip,
                limit=limit,
            ),
        }

    # ==========================================
    # Search with Filters
    # ==========================================

    @staticmethod
    def search(
        db: Session,
        organization_id: str,
        filters: InventoryFilter,
    ):

        if (
            filters.min_quantity is not None
            and filters.max_quantity is not None
            and filters.min_quantity > filters.max_quantity
        ):
            raise ValueError(
                "Minimum quantity cannot be greater than maximum quantity."
            )

        if (
            filters.low_stock_only
            and filters.out_of_stock_only
        ):
            raise ValueError(
                "Cannot combine low_stock_only with out_of_stock_only."
            )

        total, items = InventoryRepository.search(
            db,
            organization_id,
            filters,
        )

        return {
            "total": total,
            "items": items,
        }

    # ==========================================
    # Get Product Inventory
    # ==========================================

    @staticmethod
    def get_by_product(
        db: Session,
        organization_id: str,
        product_id: str,
    ):

        product = ProductRepository.get_by_id(
            db,
            product_id,
        )

        if product is None:
            raise ValueError(
                "Product not found."
            )

        if product.organization_id != organization_id:
            raise ValueError(
                "Product does not belong to this organization."
            )

        return InventoryRepository.get_by_product(
            db,
            organization_id,
            product_id,
        )

    # ==========================================
    # Get Warehouse Inventory
    # ==========================================

    @staticmethod
    def get_by_warehouse(
        db: Session,
        organization_id: str,
        warehouse_id: str,
    ):

        warehouse = WarehouseRepository.get_by_id(
            db,
            warehouse_id,
        )

        if warehouse is None:
            raise ValueError(
                "Warehouse not found."
            )

        if warehouse.organization_id != organization_id:
            raise ValueError(
                "Warehouse does not belong to this organization."
            )

        return InventoryRepository.get_by_warehouse(
            db,
            organization_id,
            warehouse_id,
        )

    # ==========================================
    # Update Inventory Settings
    # ==========================================

    @staticmethod
    def update(
        db: Session,
        inventory_id: str,
        inventory_data: InventoryUpdate,
        organization_id: str,
        user_id: str,
    ):

        inventory = InventoryService.get_by_id(
            db,
            inventory_id,
            organization_id,
        )

        if inventory is None:
            raise ValueError(
                "Inventory not found."
            )

        update_data = inventory_data.model_dump(
            exclude_unset=True
        )

        new_quantity = update_data.get(
            "quantity",
            inventory.quantity,
        )

        new_reserved_quantity = update_data.get(
            "reserved_quantity",
            inventory.reserved_quantity,
        )

        new_max_stock_level = update_data.get(
            "max_stock_level",
            inventory.max_stock_level,
        )

        if new_reserved_quantity > new_quantity:
            raise ValueError(
                "Reserved quantity cannot exceed stock quantity."
            )

        if (
            new_max_stock_level > 0
            and new_quantity > new_max_stock_level
        ):
            raise ValueError(
                "Quantity cannot exceed maximum stock level."
            )

        for key, value in update_data.items():
            setattr(
                inventory,
                key,
                value,
            )

        inventory.updated_by = user_id

        return InventoryRepository.update(
            db,
            inventory,
        )

    # ==========================================
    # Stock Adjustment
    # ==========================================

    @staticmethod
    def adjust_stock(
        db: Session,
        inventory_id: str,
        adjustment: StockAdjustment,
        organization_id: str,
        user_id: str,
    ):
        try:
            inventory = InventoryService.get_by_id(
                db=db,
                inventory_id=inventory_id,
                organization_id=organization_id,
            )

            if inventory is None:
                raise ValueError(
                    "Inventory not found."
                )

            # ==========================================
            # Validate Adjustment
            # ==========================================

            if adjustment.quantity == 0:
                raise ValueError(
                    "Adjustment quantity cannot be zero."
                )

            quantity_before = inventory.quantity

            quantity_after = (
                quantity_before
                + adjustment.quantity
            )

            # ==========================================
            # Prevent Negative Stock
            # ==========================================

            if quantity_after < 0:
                raise ValueError(
                    "Stock quantity cannot become negative."
                )

            # ==========================================
            # Prevent Reserved Stock Violation
            # ==========================================

            if (
                inventory.reserved_quantity
                > quantity_after
            ):
                raise ValueError(
                    "Stock adjustment would make reserved quantity greater than stock."
                )

            # ==========================================
            # Maximum Stock Validation
            # ==========================================

            if (
                inventory.max_stock_level > 0
                and quantity_after
                > inventory.max_stock_level
            ):
                raise ValueError(
                    "Stock quantity cannot exceed maximum stock level."
                )

            # ==========================================
            # Determine Movement Type
            # ==========================================

            if adjustment.quantity > 0:

                movement_type = (
                    InventoryMovementType.ADJUSTMENT_IN
                )

            else:

                movement_type = (
                    InventoryMovementType.ADJUSTMENT_OUT
                )

            # ==========================================
            # Update Inventory
            # ==========================================

            inventory.quantity = quantity_after
            inventory.updated_by = user_id

            InventoryRepository.update(
                db=db,
                inventory=inventory,
                commit=False,
            )

            # ==========================================
            # Create Movement
            # ==========================================

            InventoryMovementService.create(
                db=db,

                organization_id=organization_id,

                inventory_id=inventory.id,

                product_id=inventory.product_id,

                warehouse_id=inventory.warehouse_id,

                movement_type=movement_type,

                quantity=adjustment.quantity,

                quantity_before=quantity_before,

                quantity_after=quantity_after,

                user_id=user_id,

                reason=adjustment.reason,

                reference_type="INVENTORY_ADJUSTMENT",

                reference_id=inventory.id,

                commit=False,
            )

            # ==========================================
            # Atomic Commit
            # ==========================================

            db.commit()

            db.refresh(inventory)

            return inventory

        except ValueError:
            db.rollback()
            raise

        except Exception:
            db.rollback()
            raise

    # ==========================================
    # Stock Transfer
    # ==========================================

    @staticmethod
    def transfer_stock(
        db: Session,
        transfer: StockTransfer,
        organization_id: str,
        user_id: str,
    ):
        try:

            # ==========================================
            # Basic Validation
            # ==========================================

            if (
                transfer.from_warehouse_id
                == transfer.to_warehouse_id
            ):
                raise ValueError(
                    "Source and destination warehouses must be different."
                )

            # ==========================================
            # Validate Source Warehouse
            # ==========================================

            source_warehouse = WarehouseRepository.get_by_id(
                db,
                transfer.from_warehouse_id,
            )

            if source_warehouse is None:
                raise ValueError(
                    "Source warehouse not found."
                )

            if source_warehouse.organization_id != organization_id:
                raise ValueError(
                    "Source warehouse does not belong to this organization."
                )

            if not source_warehouse.is_active:
                raise ValueError(
                    "Source warehouse is inactive."
                )

            # ==========================================
            # Validate Destination Warehouse
            # ==========================================

            destination_warehouse = WarehouseRepository.get_by_id(
                db,
                transfer.to_warehouse_id,
            )

            if destination_warehouse is None:
                raise ValueError(
                    "Destination warehouse not found."
                )

            if destination_warehouse.organization_id != organization_id:
                raise ValueError(
                    "Destination warehouse does not belong to this organization."
                )

            if not destination_warehouse.is_active:
                raise ValueError(
                    "Destination warehouse is inactive."
                )

            # ==========================================
            # Validate Product
            # ==========================================

            product = ProductRepository.get_by_id(
                db,
                transfer.product_id,
            )

            if product is None:
                raise ValueError(
                    "Product not found."
                )

            if product.organization_id != organization_id:
                raise ValueError(
                    "Product does not belong to this organization."
                )

            # ==========================================
            # Get Source Inventory
            # ==========================================

            source_inventory = (
                InventoryRepository
                .get_by_product_and_warehouse(
                    db,
                    organization_id,
                    transfer.product_id,
                    transfer.from_warehouse_id,
                )
            )

            if source_inventory is None:
                raise ValueError(
                    "Source inventory record not found."
                )

            # ==========================================
            # Check Available Stock
            # ==========================================

            if (
                source_inventory.available_quantity
                < transfer.quantity
            ):
                raise ValueError(
                    "Insufficient available stock."
                )

            # ==========================================
            # Get Destination Inventory
            # ==========================================

            destination_inventory = (
                InventoryRepository
                .get_by_product_and_warehouse(
                    db,
                    organization_id,
                    transfer.product_id,
                    transfer.to_warehouse_id,
                )
            )

            # ==========================================
            # Check Destination Maximum
            # ==========================================

            if destination_inventory:

                new_destination_quantity = (
                    destination_inventory.quantity
                    + transfer.quantity
                )

                if (
                    destination_inventory.max_stock_level > 0
                    and new_destination_quantity
                    > destination_inventory.max_stock_level
                ):
                    raise ValueError(
                        "Transfer would exceed destination maximum stock level."
                    )

            # ==========================================
            # Modify Source
            # ==========================================

            source_before = source_inventory.quantity

            source_inventory.quantity -= (
                transfer.quantity
            )

            source_inventory.updated_by = user_id

            # ==========================================
            # Modify Destination
            # ==========================================

            destination_before = (
                destination_inventory.quantity
                if destination_inventory is not None
                else 0
            )

            if destination_inventory is None:

                destination_inventory = Inventory(
                    id=str(uuid4()),
                    organization_id=organization_id,
                    warehouse_id=transfer.to_warehouse_id,
                    product_id=transfer.product_id,
                    quantity=transfer.quantity,
                    reserved_quantity=0,
                    reorder_level=0,
                    max_stock_level=0,
                    created_by=user_id,
                    updated_by=user_id,
                )

                db.add(destination_inventory)

            else:

                destination_inventory.quantity += (
                    transfer.quantity
                )

                destination_inventory.updated_by = user_id

            # ==========================================
            # Record Movements
            # ==========================================

            InventoryMovementService.create(
                db=db,

                organization_id=organization_id,

                inventory_id=source_inventory.id,

                product_id=transfer.product_id,

                warehouse_id=transfer.from_warehouse_id,

                movement_type=(
                    InventoryMovementType.TRANSFER_OUT
                ),

                quantity=-(transfer.quantity),

                quantity_before=source_before,

                quantity_after=source_inventory.quantity,

                user_id=user_id,

                reason=transfer.reason,

                reference_type="INVENTORY_TRANSFER",

                reference_id=destination_inventory.id,

                commit=False,
            )

            InventoryMovementService.create(
                db=db,

                organization_id=organization_id,

                inventory_id=destination_inventory.id,

                product_id=transfer.product_id,

                warehouse_id=transfer.to_warehouse_id,

                movement_type=(
                    InventoryMovementType.TRANSFER_IN
                ),

                quantity=transfer.quantity,

                quantity_before=destination_before,

                quantity_after=destination_inventory.quantity,

                user_id=user_id,

                reason=transfer.reason,

                reference_type="INVENTORY_TRANSFER",

                reference_id=source_inventory.id,

                commit=False,
            )

            # ==========================================
            # SINGLE COMMIT
            # ==========================================

            db.commit()

            db.refresh(source_inventory)
            db.refresh(destination_inventory)

            return {
                "message": "Stock transferred successfully.",
                "product_id": transfer.product_id,
                "from_warehouse_id": transfer.from_warehouse_id,
                "to_warehouse_id": transfer.to_warehouse_id,
                "quantity": transfer.quantity,
            }

        except ValueError:
            db.rollback()
            raise

        except Exception:
            db.rollback()
            raise

    # ==========================================
    # Low Stock
    # ==========================================

    @staticmethod
    def get_low_stock(
        db: Session,
        organization_id: str,
    ):

        return InventoryRepository.get_low_stock(
            db,
            organization_id,
        )

    # ==========================================
    # Delete
    # ==========================================

    @staticmethod
    def delete(
        db: Session,
        inventory_id: str,
        organization_id: str,
    ):

        inventory = InventoryService.get_by_id(
            db,
            inventory_id,
            organization_id,
        )

        if inventory is None:
            raise ValueError(
                "Inventory not found."
            )

        # Do not allow deletion if stock exists
        if inventory.quantity > 0:
            raise ValueError(
                "Inventory with existing stock cannot be deleted."
            )

        # Do not allow deletion if stock is reserved
        if inventory.reserved_quantity > 0:
            raise ValueError(
                "Inventory with reserved stock cannot be deleted."
            )

        InventoryRepository.delete(
            db,
            inventory,
        )

        return {
            "message": "Inventory deleted successfully."
        }